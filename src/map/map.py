import os
import pygame
import sys

import TileFactory

from tiles.Tile import Tile
from linkEvent import LinkEvent
from dialogEvent import DialogEvent
from player.player import Player
import random
from visitor.visitor import Visitor
from tiles.visitorTile import VisitorTile
from zookeeper.zookeeper import Zookeeper
from Queue import Queue
from visitor.splat import Splat
from cutscene import Cutscene
from utils import image_util

class Map:
    tile_size = 32   
    
    def __init__(self, name,screen,game):
        # Make the full pathname of the map
        self.fullname = os.path.join('map', 'maps', name)
        
        self.tiles = []
        
        self.splat_idx = 0
        self.max_splats = 20
        self.splats = []
          
        self.game_objects = pygame.sprite.Group()
        self.unjumpable_objects = pygame.sprite.Group()
        self.unwalkable_tiles = pygame.sprite.Group()
        self.unswimmable_and_unwalkable_tiles = pygame.sprite.Group()
        self.unjumpable_tiles = pygame.sprite.Group()
        self.high_level = pygame.sprite.Group()
        self.loaded_cutscenes = dict()
        
        self.screen=screen
        self.game=game
        
        self.events = dict()
        
        self.visitor_spawn_rate = 1000
        self.num_visitors = 0
        self.max_visitors = 50
        
        self.zookeeper_spawn_rate= 1000
        self.num_zookeepers = 0
        self.max_zookeepers = 5
        
        self.first_visible_x = 0
        self.last_visible_x = 0
        self.first_visible_y = 0
        self.last_visible_y = 0
        
        self.width = 0
        self.height = 0
        
        self.start_cutscenes = []
        self.played_cutscenes = dict()
        
        self.press_enter = image_util.load_sliced_sprites(210, 80, os.path.join("cutscenes","press_enter.png"))

    def intialize(self):
        file = open(self.fullname, 'r')
        self.load_map(file)

    def fire_tile(self, index, source):
        if index in self.events:
            if isinstance(self.events[index], Cutscene):
                if self.played_cutscenes[self.events[index].name]:
                    return
                else:
                    self.played_cutscenes[self.events[index].name] = True
            return self.events[index].fire(source)
        return True

    def add_splat(self, x, y):
        splat = Splat(x,y,self.game)
        self.splats.append(splat)
        if len(self.splats) >= self.max_splats:
            self.splats.pop(0)

    def update_objects(self):
        # generate new visitors
        
        for obj in self.game_objects:
            x = obj.x/32
            y = obj.y/32
            if (x >= self.first_visible_x and x <= self.last_visible_x) and \
               (y >= self.first_visible_y and y <= self.last_visible_y):
                obj.update()
        
        self.first_visible_x = (self.game.player.x - (self.game.map_screen.get_width()/2))/32
        self.last_visible_x = (self.game.player.x + (self.game.map_screen.get_width()/2))/32
        self.first_visible_y = (self.game.player.y - (self.game.map_screen.get_height()/2))/32
        self.last_visible_y = (self.game.player.y + (self.game.map_screen.get_height()/2))/32 
        
        if self.num_visitors < self.max_visitors:
            x = random.randint(0,self.tiles_wide-1);
            y = random.randint(0,self.tiles_high-1);
            if (x < self.first_visible_x or x > self.last_visible_x) and (y < self.first_visible_y or y >self. last_visible_y):
                if isinstance(self.tiles[y*self.tiles_wide + x], VisitorTile):
                    pick = random.randint(0,2)
                    visitor = None
                    if pick is 0:
                        visitor = TileFactory.generateSprite("V", x, y, self.game);
                    elif pick is 1:
                        visitor = TileFactory.generateSprite("V2", x, y, self.game);
                    else:
                        visitor = TileFactory.generateSprite("V3", x, y, self.game);
                    self.game_objects.add(visitor)
                  
        if self.num_zookeepers < self.max_zookeepers:
            x = random.randint(0,self.tiles_wide-1);
            y = random.randint(0,self.tiles_high-1);
            if (x < self.first_visible_x or x > self.last_visible_x) and (y < self.first_visible_y or y > self.last_visible_y):
                if isinstance(self.tiles[y*self.tiles_wide + x], VisitorTile):
                    zookeeper = TileFactory.generateSprite("Z", x, y, self.game);
                    self.game_objects.add(zookeeper)
            
    def draw_tiles(self):
        for tile in self.tiles:
            if (tile.x >= self.first_visible_x and tile.x <= self.last_visible_x) and \
               (tile.y >= self.first_visible_y and tile.y <= self.last_visible_y):
                tile.draw()
            
        for splat in self.splats:
                splat.draw()
                
        for cutscene in self.start_cutscenes:
            self.start_cutscenes.remove(cutscene)
            cutscene.fire(self.game.player)
        
    def draw_objects(self):
        for obj in self.game_objects:
            x = obj.x/32
            y = obj.y/32
            if (x + obj.image.get_width()/32 >= self.first_visible_x and x <= self.last_visible_x) and \
               (y + obj.image.get_height()/32 >= self.first_visible_y and y <= self.last_visible_y):
                obj.draw()
    
    # Load the map from the text file
    # Maps are comma separated value files
    # where each value is an index into the array found
    # in TileFactory.py.
    def load_map(self, file):
        lines = file.readlines()
        
        # Load the tile map
        
        for idx in xrange(len(lines)):
            line = lines[idx]
            if line == " \n":
                self.tiles_high = idx
                self.height = self.tiles_high * self.tile_size
        
        for y in xrange(0, self.tiles_high):
            line = lines[y]
            
            parsed_comments = line.split('#');
            
            line_tiles = parsed_comments[0].replace(' ','').replace('\n','').split(',')
            
            self.tiles_wide = len(line_tiles)
            self.width = self.tiles_wide * self.tile_size
            self.num_tiles = self.tiles_wide * self.tiles_high
            
            x = 0
            for key in line_tiles:
                tile = TileFactory.generateTile(key,x,y,self.game) 
                self.tiles.append(tile)
                if not tile.walkable:
                    self.unwalkable_tiles.add(tile)
                if not tile.visible:
                    self.unjumpable_tiles.add(tile)
                if not tile.swimmable and not tile.walkable:
                    self.unswimmable_and_unwalkable_tiles.add(tile)
                x += 1
               
        index = self.tiles_high 
        while lines[index] is "\n":
            index += 1
        index += 1
            
        # Load the sprite map
        for y in xrange(index, self.tiles_high + index):
            line = lines[y]
            
            parsed_comments = line.split('#');
            
            line_tiles = parsed_comments[0].replace(' ','').replace('\n','').split(',')
            
            x = 0
            for key in line_tiles:
                if key is not None and key is not '':
                    object = TileFactory.generateSprite(key,x,y - index,self.game)
                    #if not isinstance(object, Player):
                    self.game_objects.add( object )
                x += 1
        
        # special commands        
        index = self.tiles_high + index
        while index < len(lines):
            if lines[index] is "\n":
                index += 1
                continue
            
            command = lines[index].split(' ')
            
            if command[0] == 'link':
                start_coords = command[1].split(',')
                end_map = command[2]
                end_coords = command[3].split(',')
                self.events[int(start_coords[1])*self.tiles_wide+int(start_coords[0])] = LinkEvent(start_coords, end_coords, end_map, self.game)
            elif command[0] == 'dialog':
                start_coords = command[1].split(',')
                text = " ".join(command[2:])
                self.events[int(start_coords[1])*self.tiles_wide+int(start_coords[0])] = DialogEvent(text, self.game)
            elif command[0] == 'cutscene':
                slides = []
                for image in [os.path.join("cutscenes",image).replace('\n','') for image in command[3:]]:
                    if(self.loaded_cutscenes.has_key(image)):
                        slides.append(self.loaded_cutscenes.get(image))
                    else:
                        loaded_image = image_util.load_image(image) 
                        slides.append(loaded_image)
                        self.loaded_cutscenes[image] = loaded_image
                    
                cutscene = Cutscene(self.game, command[2], slides, self.press_enter)
                self.played_cutscenes[cutscene.name] = False
                if command[1] == "start":
                    self.start_cutscenes.append(cutscene)
                else:
                    coords = command[1].split(',')
                    self.events[int(coords[1])*self.tiles_wide+int(coords[0])] = cutscene
  
            index += 1
            
        
