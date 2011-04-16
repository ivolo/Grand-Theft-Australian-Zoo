'''
The main gameloop
'''

import sys, os
import pygame
from pygame.locals import *

from player.Player import Player
from map.Map import Map
from player.taz import Taz

class Game:

    screen_dim = 640, 480
    
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
        
        self.player = Taz(self, 0, 0)
        
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( False )
            
        self.loadLevel("sample_map.txt")
    
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
    
    def gameloop(self):
        while(True):
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
                pass
    
    def getButtonPresses(self):
        keys = pygame.key.get_pressed()

        if(keys[K_ESCAPE]):
            if not self.pressed[K_ESCAPE]:
                sys.exit()
        else:
            self.pressed[K_ESCAPE] = False
    
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
        return
    
    def draw(self):
        if self.current_map is not None:
            self.current_map.draw_tiles()
            self.current_map.draw_objects()
            
        self.player.draw()
        
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.gameloop()



