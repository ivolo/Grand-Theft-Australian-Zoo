'''
Created on Apr 29, 2011

@author: krakauer
'''
import sys
import pygame
from pygame.locals import *

from utils import image_util
from gameloop import Game
from menus.controlScreen import ControlScreen
from menus.creditsScreen import CreditsScreen

PLAY = 0
OPTIONS = 1
CONTROLS = 2
QUIT = 3
MAX_INDEX = 3

class MenuScreen:
    
    def __init__(self):
        self.game = Game()
        self.screen = self.game.screen
        self.image = image_util.load_image("mainmenu.png")
        
        self.index = 0
    
        self.play_rect = Rect(275,200,245,70)
        self.options_rect = Rect(275,290,245,70)
        self.controls_rect = Rect(275,380,245,70)
        self.quit_rect = Rect(275,470,245,70)
        
        self.credits_rect = Rect(610, 530, 180, 60)
        
        self.controlScreen = ControlScreen(self.game)
        self.creditsScreen = CreditsScreen(self.game)
        
        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( True )
    
    def get_input(self):
        self.getEvents()
        self.getButtonPresses()
    
    def getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.play_rect.collidepoint(pos):
                    self.index = PLAY
                    self.draw()
                    self.play()
                elif self.options_rect.collidepoint(pos):
                    self.index = OPTIONS
                    self.draw()
                    self.options()
                elif self.controls_rect.collidepoint(pos):
                    self.index = CONTROLS
                    self.draw()
                    self.controls()
                elif self.quit_rect.collidepoint(pos):
                    self.index = QUIT
                    self.quit()
                elif self.credits_rect.collidepoint(pos):
                    self.credits()
    
    def getButtonPresses(self):
        keys = pygame.key.get_pressed()

        # select
        if(keys[K_SPACE]):
            if not self.pressed[K_SPACE]:
                self.pressed[K_SPACE] = True
                self.select()
        else:
            self.pressed[K_SPACE] = False

        if(keys[K_RETURN]):
            if not self.pressed[K_RETURN]:
                self.pressed[K_RETURN] = True
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

    def play(self):
        self.game.gameloop()
        for x in xrange(len(self.pressed)):
            self.pressed[x] = True
    
    def options(self):
        pass
    
    def controls(self):
        self.controlScreen.loop()
        for x in xrange(len(self.pressed)):
            self.pressed[x] = True
    
    def quit(self):
        sys.exit()

    def credits(self):
        self.creditsScreen.loop()
        for x in xrange(len(self.pressed)):
            self.pressed[x] = True

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
        if self.index is PLAY:
            self.play()
        elif self.index is OPTIONS:
            self.options()
        elif self.index is CONTROLS:
            self.controls()
        elif self.index is QUIT:
            self.quit()

    def draw(self):
        self.screen.blit(self.image, (0,0))
        
        if self.index is PLAY:
            pygame.draw.rect(self.screen, (255,255,0), self.play_rect, 5)
        elif self.index is OPTIONS:
            pygame.draw.rect(self.screen, (255,255,0), self.options_rect, 5)
        elif self.index is CONTROLS:
            pygame.draw.rect(self.screen, (255,255,0), self.controls_rect, 5)
        elif self.index is QUIT:
            pygame.draw.rect(self.screen, (255,255,0), self.quit_rect, 5)
            
        pygame.display.flip()
    
    def loop(self):
        while True:
            self.draw()
            self.get_input()

if __name__ == '__main__':
    menu = MenuScreen()
    menu.loop()