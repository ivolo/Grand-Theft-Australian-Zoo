import os
import pygame
import sys

import TileFactory

from tiles.Tile import Tile
from linkEvent import LinkEvent
from player.player import Player
import random
from visitor.visitor import Visitor
from tiles.visitorTile import VisitorTile
from zookeeper.zookeeper import Zookeeper

class Map:
    tile_size = 32   
    
    def __init__(self, name,screen,game):
        # Make the full pathname of the map
        self.fullname = os.path.join('map', 'maps', name)
        
        
        self.tiles = []
        self.game_objects = pygame.sprite.Group()
        self.unwalkable_tiles = pygame.sprite.Group()
        
        self.screen=screen
        self.game=game
        
        self.events = dict()
        
        self.visitor_spawn_rate = 1000
        self.num_visitors = 0
        self.max_visitors = 50
        
        self.zookeeper_spawn_rate= 1000
        self.num_zookeepers = 0
        self.max_zookeepers = 5
        
        #self.tiles_wide = screen.get_width()/self.tile_size
        #self.tiles_high = screen.get_height()/self.tile_size
        #self.num_tiles = self.tiles_wide * self.tiles_high

    def intialize(self):
        file = open(self.fullname, 'r')
        self.load_map(file)

    def fire_tile(self, index, source):
        if index in self.events:
            self.events[index].fire(source)

    def update_objects(self):
        # generate new visitors
        
        first_visible_x = (self.game.player.x - (self.game.map_screen.get_width()/2))/32
        last_visible_x = (self.game.player.x + (self.game.map_screen.get_width()/2))/32
        first_visible_y = (self.game.player.y - (self.game.map_screen.get_height()/2))/32
        last_visible_y = (self.game.player.y + (self.game.map_screen.get_height()/2))/32 
        
        if self.num_visitors < self.max_visitors:
            spawn_visitor = random.randint(0,1000)
            if spawn_visitor < self.visitor_spawn_rate:
                x = random.randint(0,self.tiles_wide-1);
                y = random.randint(0,self.tiles_high-1);
                if (x < first_visible_x or x > last_visible_x) and (y < first_visible_y or y > last_visible_y):
                    if isinstance(self.tiles[y*self.tiles_wide + x], VisitorTile):
                        visitor = Visitor(x, y, self.game);
                        self.game_objects.add(visitor)
                        
        if self.num_zookeepers < self.max_zookeepers:
            spawn_keeper = random.randint(0,1000)
            if spawn_keeper < self.zookeeper_spawn_rate:
                x = random.randint(0,self.tiles_wide-1);
                y = random.randint(0,self.tiles_high-1);
                if (x < first_visible_x or x > last_visible_x) and (y < first_visible_y or y > last_visible_y):
                    if isinstance(self.tiles[y*self.tiles_wide + x], VisitorTile):
                        zookeeper = Zookeeper(x, y, self.game);
                        self.game_objects.add(zookeeper)
        
        for obj in self.game_objects:
            obj.update()
            
    def draw_tiles(self):
        for tile in self.tiles:
            tile.draw()
        
    def draw_objects(self):
        for obj in self.game_objects:
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
        
        for y in xrange(0, self.tiles_high):
            line = lines[y]
            
            parsed_comments = line.split('#');
            
            line_tiles = parsed_comments[0].replace(' ','').replace('\n','').split(',')
            
            self.tiles_wide = len(line_tiles)
            self.num_tiles = self.tiles_wide * self.tiles_high
            
            x = 0
            for key in line_tiles:
                tile = TileFactory.generateTile(key,x,y,self.game) 
                self.tiles.append(tile)
                if not tile.walkable:
                    self.unwalkable_tiles.add(tile)
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
                    if not isinstance(object, Player):
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
            
            index += 1
            
        
