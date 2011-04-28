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

class Game:

    screen_dim = 800,576
    
    loaded_maps = {}
    current_map = None
    
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.screen_dim)
        self.screen = pygame.display.get_surface()
        self.map_screen = self.screen.subsurface(0, 0, self.screen_dim[0], self.screen_dim[1])
        #pygame.display.set_icon(pygame.image.load(os.path.join("images", "ui","icon.png")))
        pygame.display.set_caption("Grand Theft Australian Zoo")
        pygame.mouse.set_visible(1);        
        
        self.cursor = Sprite()
        self.cursor.rect = Rect(0,0,1,1)
        
        self.player_group = Group()
        self.player = Kangaroo(1, 1, self)
        self.player.inUse = True
        self.player.current_image = self.player.image
        self.clock = pygame.time.Clock()
        
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( False )
            
        self.loadLevel("inn.txt")
        
    def reset(self):
        self.player_group.remove(self.player)
        self.player = self.player.newPlayer()
        self.player.current_image = self.player.image
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( False )
            
        self.loadLevel("large_map.txt")
    
    def loadLevel(self, file):
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( False )
        
        if file in self.loaded_maps:
            self.current_map = self.loaded_maps[file]
        else:
            self.current_map = Map(file, self.screen, self)
            self.loaded_maps[file] = self.current_map
            self.current_map.intialize()
    
    def change_maps(self, dest, x, y):
        self.loadLevel(dest)
        self.player.x = x * 32
        self.player.y = y * 32
        self.player.rect.left = self.player.x + self.player.left_offset
        self.player.rect.top = self.player.y + self.player.top_offset
    
    def change_player(self, newPlayer):
        self.player.inUse = False
        self.player.leave_car()
        self.player = newPlayer;
        self.player.inUse = True
        self.player.current_image = self.player.image
    
    def gameloop(self):
        while(True):
            self.clock.tick(60)
            self.get_input()
            self.update_state()
            self.draw()
        return
    
    def get_input(self):
        self.getEvents()
        self.getButtonPresses()
        return
    
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x_diff = self.player.x - (self.map_screen.get_width() / 2)
                y_diff = self.player.y - (self.map_screen.get_height() / 2)
                self.cursor.rect.left = pos[0] + x_diff
                self.cursor.rect.top = pos[1] + y_diff
                collision = pygame.sprite.spritecollideany(self.cursor, self.player_group)
                if collision != None:
                    self.change_player(collision)
    
    def getButtonPresses(self):
        keys = pygame.key.get_pressed()

        # quit
        if(keys[K_ESCAPE]):
            if not self.pressed[K_ESCAPE]:
                sys.exit()
        else:
            self.pressed[K_ESCAPE] = False
    
        # attack
        if(keys[K_SPACE]):
            if not self.pressed[K_SPACE]:
                self.player.attack()
        else:
            self.pressed[K_SPACE] = False
    
        # use ability
        if(keys[K_RETURN]):
            if not self.pressed[K_RETURN]:
                self.player.use_ability()
        else:
            self.pressed[K_RETURN] = False
    
        # get into car
        if(keys[K_UP]):
            if not self.pressed[K_UP]:
                self.player.get_into_car()
        else:
            self.pressed[K_UP] = False
        
        # get out of car
        if(keys[K_DOWN]):
            if not self.pressed[K_DOWN]:
                self.player.leave_car()
        else:
            self.pressed[K_DOWN] = False
        
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
        
    
    def update_state(self):
        if self.current_map is not None:
            self.current_map.update_objects()
            
        for p in self.player_group:
            p.update()
    
    def draw(self):
        self.map_screen.fill((0,0,0))
        if self.current_map is not None:
            self.current_map.draw_tiles()
            self.current_map.draw_objects()
        
        for p in self.player_group:
            p.draw()
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.gameloop()



