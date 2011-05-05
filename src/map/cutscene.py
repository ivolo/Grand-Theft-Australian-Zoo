import sys, os
import pygame
from pygame.locals import *
from utils import image_util
from mapEvent import MapEvent
from pygame import time

class Cutscene(MapEvent):
    
    def __init__(self, game, name, slides, press_enter):
        '''
        Slides is an array list of strings (the files that make up the slides).
        '''
        self.name = name
        
        self.images = slides #[image_util.load_image(slide)for slide in slides]
        self.slide = 0
        self.done = False
        self.game = game
        self.clock = pygame.time.Clock()
        self.screen = game.screen
        
        self.press_enter = press_enter
        self.current_press_enter_index = 0
        self.start_time = time.get_ticks()
        self.last_change = self.start_time
        self.wait_time = 200
        
        self.game = game
        
        self.soundUtil.LoadSound('jungle.wav', "jungle")
        self.soundUtil.PlaySound("jungle")
        
        #if not pygame.mixer: print 'Warning, sound disabled'

        self.pressed = []
        for key in pygame.key.get_pressed():
            self.pressed.append( True )
    
    def change_slide(self):
        self.slide += 1
        if self.slide < len(self.images):
            self.draw()
            #if self.sounds[self.slide] is not None:
            #    self.game.soundUtil.LoadSound(self.sounds[self.slide], "slideshow")
            #    self.game.soundUtil.PlaySound("slideshow")
        
    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        
        keys = pygame.key.get_pressed()
        
        if(keys[K_RETURN]):
            if not self.pressed[K_RETURN]:
                self.pressed[K_RETURN] = True
                self.change_slide()
        else:
            self.pressed[K_RETURN] = False
        
        if self.slide is len(self.images):
            self.done = True;
            #self.game.soundUtil.StopSound("slideshow")
            return
        
        if time.get_ticks() > self.last_change + self.wait_time:
            self.current_press_enter_index += 1
            if self.current_press_enter_index >= len(self.press_enter):
                self.current_press_enter_index = 0
            self.last_change = time.get_ticks()
    
    def draw(self):
        if self.slide is len(self.images):
            return
        
        self.game.draw_without_flip()
        
        self.screen.blit(self.images[self.slide], (0,0))
        
        self.screen.blit(self.press_enter[self.current_press_enter_index], (575,20))
        
        pygame.display.flip()
        
    def fire(self, source):
        if source is not self.game.player:
            return True
        
        while self.done is False:
            self.update()
            self.draw()
        return True