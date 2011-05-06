'''
Created on May 5, 2011

@author: krakauer
'''
import pygame
from game_objects.gameObject import GameObject
from game_constants.client import TILE_SIZE

class Key(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Key, self).__init__(image, (x*TILE_SIZE, y*TILE_SIZE), game)
        self.left_offset = 0
        self.top_offset = 0
      
    def update(self):
        rectangle = pygame.Rect(self.game.player.x, self.game.player.y, TILE_SIZE, TILE_SIZE)
        
        if self.rect.colliderect(rectangle):
            self.game.hasKey = True
            self.kill()
            self.game.hud.draw()
    