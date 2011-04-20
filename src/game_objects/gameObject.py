'''
Created on Apr 15, 2011

@author: calvin
'''
import pygame

from utils.sprite_util import check_collision

class GameObject(pygame.sprite.Sprite):
    
    def __init__(self, image, coordinates, game):
        super(GameObject, self).__init__()
        
        self.x, self.y = coordinates
        
        self.game = game
        
        self.image = image
        
        self.rect = self.image.get_rect().move(coordinates)
        
        self.screen = game.screen
        
        self.shouldRemove = False
        
    def move(self, x_change, y_change):
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
            
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
            
        self.x = self.rect.left
        self.y = self.rect.top
        
    def update(self):
        raise NotImplementedError();

    def draw(self):
        raise NotImplementedError();