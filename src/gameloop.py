'''
The main gameloop
'''

import sys, os
import pygame
from pygame.locals import *

from player.player import Player
from map.map import Map
from player.taz import Taz
from pygame.sprite import Group, Sprite
from player.kangaroo import Kangaroo
from player.snake import Snake

from game_constants.client import *
from hud.hud import Hud
from hud import animal_info
from game_variables import animals_freed
from utils import image_util
from menus.pauseScreen import PauseScreen, CONTINUE, MAIN_MENU
from car.imperviousCar import ImperviousCar
from car.car import Car
from player.koala import Koala
from player.taz import Taz
from player.dingo import Dingo
from utils.sound_util import SoundUtil

class Game:
    
    loaded_maps = {}
    current_map = None
    
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = pygame.display.get_surface()
        self.map_screen = self.screen.subsurface(0, 0, MAP_WIDTH, MAP_HEIGHT)
        #pygame.display.set_icon(pygame.image.load(os.path.join("images", "ui","icon.png")))
        pygame.display.set_caption("Grand Theft Australian Zoo")
        pygame.mouse.set_visible(1);        
        
        self.soundUtil = SoundUtil()
        self.soundUtil.sound_on = True
        
        self.pauseMenu = PauseScreen(self)
        
        self.cursor = Sprite()
        self.cursor.rect = Rect(0,0,1,1)
        
        self.hud = Hud(self)
        
        self.player_group = Group()
        self.player = Taz(image_util.load_image("tasmanian.png"), 1, 1, self)
        self.player.inUse = True
        self.player.current_image = self.player.image
        
        self.hud.set_player(self.player)
        
        self.clock = pygame.time.Clock()
        
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( True )
            
        self.loadLevel("zookeeperland.txt")
        
        self.returnToMainMenu = False
        
    def reset(self):
        self.player_group.remove(self.player)
        self.current_map.game_objects.remove(self.player)
        self.player = self.player.newPlayer()
        self.player.inUse = True
        self.player.current_image = self.player.image
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( False )
            
        self.loadLevel("jail.txt")
        self.player.x = TILE_SIZE
        self.player.y = TILE_SIZE
        self.player.rect.left = self.player.x + self.player.left_offset
        self.player.rect.top = self.player.y + self.player.top_offset
    
    def loadLevel(self, file):
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( False )
        
        if file in self.loaded_maps:
            self.current_map = self.loaded_maps[file]
            self.current_map.reset()
        else:
            self.current_map = Map(file, self.screen, self)
            self.loaded_maps[file] = self.current_map
            self.current_map.intialize()
    
    def change_maps(self, dest, x, y):
        if self.player.isInCar:
            self.current_map.game_objects.remove(self.player.car)
            self.current_map.not_player.remove(self.player.car)
        
        self.loadLevel(dest)
        self.player.x = x * TILE_SIZE
        self.player.y = y * TILE_SIZE
        self.player.rect.left = self.player.x + self.player.left_offset
        self.player.rect.top = self.player.y + self.player.top_offset
        
        if self.player.isInCar:
            if isinstance(self.player.car, ImperviousCar):
                self.player.car = Car(None,0,0,self)
                self.player.car.driver = self.player
                self.player.car.driving = True
            self.player.car.x = x * TILE_SIZE
            self.player.car.y = y * TILE_SIZE
            self.player.car.rect.left = self.player.car.x
            self.player.car.rect.top = self.player.car.y
            self.player.car.avoidMapLinks()
            self.current_map.game_objects.add(self.player.car)
        elif self.player.isInTree:
            self.player.getOutOfTree()
            self.player.x = TILE_SIZE
            self.player.y = TILE_SIZE
            self.player.rect.left = self.player.x + self.player.left_offset
            self.player.rect.top = self.player.y + self.player.top_offset
    
    def change_player(self, newPlayer):
        self.player.inUse = False
        self.player.leave_car()
        self.current_map.game_objects.add(self.player)
        self.player = newPlayer;
        self.player.inUse = True
        self.player.current_image = self.player.image
        self.hud.set_player(self.player)
    
    def free_animal(self, animal_name):
        animals_freed[animal_name] = image_util.load_image(animal_info.info[animal_name][3])
        self.hud.draw()
    
    def gameloop(self):
        self.returnToMainMenu = False
        self.hud.draw()
        while self.returnToMainMenu is False:
            self.clock.tick(60)
            self.get_input()
            self.update_state()
            self.draw()
    
    def get_input(self):
        self.getEvents()
        self.getButtonPresses()
        return
    
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
    
    def getButtonPresses(self):
        keys = pygame.key.get_pressed()

        # quit
        if(keys[K_ESCAPE]):
            if not self.pressed[K_ESCAPE]:
                self.pressed[K_ESCAPE] = True
                self.pauseMenu.loop()
                #figure out what we wanted to do
                if self.pauseMenu.index is CONTINUE:
                    self.hud.draw()
                elif self.pauseMenu.index is MAIN_MENU:
                    self.returnToMainMenu = True
        else:
            self.pressed[K_ESCAPE] = False
    
        # attack
        if(keys[K_SPACE]):
            if not self.pressed[K_SPACE]:
                self.pressed[K_SPACE] = True
                self.player.attack()
        else:
            self.pressed[K_SPACE] = False
    
        # use ability
        if(keys[K_RETURN]):
            if not self.pressed[K_RETURN]:
                self.pressed[K_RETURN] = True
                self.player.use_ability()
        else:
            self.pressed[K_RETURN] = False
    
        # get into and out of car
        if(keys[K_q]):
            if not self.pressed[K_q]:
                self.pressed[K_q] = True
                self.player.use_object()
        else:
            self.pressed[K_q] = False
        
        # move
        if(keys[K_w]):
            if not self.pressed[K_w]:
                self.player.move(0, -1)
        else:
            self.pressed[K_w] = False
    
        if(keys[K_s]):
            if not self.pressed[K_s]:
                self.player.move(0, 1)
        else:
            self.pressed[K_s] = False
            
        if(keys[K_a]):
            if not self.pressed[K_a]:
                self.player.move(-1, 0)
        else:
            self.pressed[K_a] = False
            
        if(keys[K_d]):
            if not self.pressed[K_d]:
                self.player.move(1, 0)
        else:
            self.pressed[K_d] = False
        
        if(keys[K_UP]):
            if not self.pressed[K_UP]:
                self.player.move(0, -1)
        else:
            self.pressed[K_UP] = False
    
        if(keys[K_DOWN]):
            if not self.pressed[K_DOWN]:
                self.player.move(0, 1)
        else:
            self.pressed[K_DOWN] = False
            
        if(keys[K_LEFT]):
            if not self.pressed[K_LEFT]:
                self.player.move(-1, 0)
        else:
            self.pressed[K_LEFT] = False
            
        if(keys[K_RIGHT]):
            if not self.pressed[K_RIGHT]:
                self.player.move(1, 0)
        else:
            self.pressed[K_RIGHT] = False
        
        if(keys[K_o]):
            if not self.pressed[K_o]:
                if self.soundUtil.sound_on:
                    self.soundUtil.sound_on = False
                else:
                    self.soundUtil.sound_on = True
        else:
            self.pressed[K_o] = False
            
            
    def update_state(self):
        if self.current_map is not None:
            self.current_map.update_objects()
            
        for p in self.player_group:
            p.update()
    
    def draw_without_flip(self):
        self.map_screen.fill((0,0,0))
        if self.current_map is not None:
            self.current_map.draw_tiles()
            self.current_map.draw_objects()
        
        #for p in self.player_group:
        #    p.draw()
        self.player.draw()
    
    def draw(self):
        self.draw_without_flip()
        for cutscene in self.current_map.start_cutscenes:
            self.current_map.start_cutscenes.remove(cutscene)
            cutscene.fire(self.player)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.gameloop()



