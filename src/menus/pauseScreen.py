'''
Created on Apr 29, 2011

@author: krakauer
'''
import sys
import pygame
from pygame.locals import *

from utils import image_util
from menus.controlScreen import ControlScreen

CONTINUE = 0
CONTROLS = 1
MAIN_MENU = 2
MAX_INDEX = 2

class PauseScreen:
    
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.image = image_util.load_image("pause_screen.png")
        
        self.index = 0
    
        self.continue_rect = Rect(275,200,245,70)
        self.controls_rect = Rect(275,290,245,70)
        self.mainmenu_rect = Rect(275,380,245,70)
        
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( True )
            
        self.unpause = False
        
        self.control_screen = ControlScreen(self.game)
    
    def get_input(self):
        self.getEvents()
        self.getButtonPresses()
    
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.continue_rect.collidepoint(pos):
                    self.index = CONTINUE
                    self.draw()
                    self.cont()
                elif self.controls_rect.collidepoint(pos):
                    self.index = CONTROLS
                    self.draw()
                    self.controls()
                elif self.mainmenu_rect.collidepoint(pos):
                    self.index = MAIN_MENU
                    self.draw()
                    self.main_menu()
    
    def getButtonPresses(self):
        keys = pygame.key.get_pressed()

        # quit
        if(keys[K_ESCAPE]):
            if not self.pressed[K_ESCAPE]:
                self.cont()
        else:
            self.pressed[K_ESCAPE] = False
    
        # select
        if(keys[K_SPACE]):
            if not self.pressed[K_SPACE]:
                self.select()
        else:
            self.pressed[K_SPACE] = False

        if(keys[K_RETURN]):
            if not self.pressed[K_RETURN]:
                self.select()
        else:
            self.pressed[K_RETURN] = False
    
        # move
        if(keys[K_UP]):
            if not self.pressed[K_UP]:
                self.pressed[K_UP] = True
                self.up()
        else:
            self.pressed[K_UP] = False
        
        if(keys[K_DOWN]):
            if not self.pressed[K_DOWN]:
                self.pressed[K_DOWN] = True
                self.down()
        else:
            self.pressed[K_DOWN] = False
        
        if(keys[K_w]):
            if not self.pressed[K_w]:
                self.pressed[K_w] = True
                self.up()
        else:
            self.pressed[K_w] = False
    
        if(keys[K_s]):
            if not self.pressed[K_s]:
                self.pressed[K_s] = True
                self.down()
        else:
            self.pressed[K_s] = False

    def cont(self):
        self.leave()
    
    
    def controls(self):
        self.control_screen.loop()
        for x in xrange(len(self.pressed)):
            self.pressed[x] = True
    
    def main_menu(self):
        self.leave()

    def up(self):
        self.index -= 1
        if self.index < 0:
            self.index = MAX_INDEX
            
        self.draw()
    
    def down(self):
        self.index += 1
        if self.index > MAX_INDEX:
            self.index = 0
            
        self.draw()
    
    def select(self):
        if self.index is CONTINUE:
            self.cont()
        elif self.index is CONTROLS:
            self.controls()
        elif self.index is MAIN_MENU:
            self.main_menu()

    def leave(self):
        for x in xrange(len(self.pressed)):
            self.pressed[x] = True
            
        self.unpause = True

    def draw(self):
        self.screen.blit(self.image, (0,0))
        
        if self.index is CONTINUE:
            pygame.draw.rect(self.screen, (255,255,0), self.continue_rect, 5)
        elif self.index is CONTROLS:
            pygame.draw.rect(self.screen, (255,255,0), self.controls_rect, 5)
        elif self.index is MAIN_MENU:
            pygame.draw.rect(self.screen, (255,255,0), self.mainmenu_rect, 5)
            
        pygame.display.flip()
    
    def loop(self):
        for x in xrange(len(self.pressed)):
            self.pressed[x] = True
        while self.unpause is False:
            self.draw()
            self.get_input()
        self.unpause = False
