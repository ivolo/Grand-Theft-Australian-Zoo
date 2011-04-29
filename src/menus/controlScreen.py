'''
Created on Apr 29, 2011

@author: krakauer
'''
import sys
import pygame
from pygame.locals import *

from utils import image_util

class ControlScreen:
    
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.image = image_util.load_image("controls.png")
    
        self.back_rect = Rect(656,540,131,55)
        
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( True )
            
        self.go_back = False
    
    def get_input(self):
        self.getEvents()
        self.getButtonPresses()
    
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.back_rect.collidepoint(pos):
                    self.back()
    
    def getButtonPresses(self):
        keys = pygame.key.get_pressed()

        # quit
        if(keys[K_ESCAPE]):
            if not self.pressed[K_ESCAPE]:
                self.back()
        else:
            self.pressed[K_ESCAPE] = False
    
        # select
        if(keys[K_SPACE]):
            if not self.pressed[K_SPACE]:
                self.back()
        else:
            self.pressed[K_SPACE] = False

        if(keys[K_RETURN]):
            if not self.pressed[K_RETURN]:
                self.back()
        else:
            self.pressed[K_RETURN] = False

    def back(self):
        for x in xrange(len(self.pressed)):
            self.pressed[x] = True
        self.go_back = True

    def draw(self):
        self.screen.blit(self.image, (0,0))
            
        pygame.display.flip()
    
    def loop(self):
        self.go_back = False
        while self.go_back is False:
            self.draw()
            self.get_input()
