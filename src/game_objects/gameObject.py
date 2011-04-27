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
        self.current_image = image
        self.rect = self.image.get_rect().move(coordinates)
        
        self.screen = game.screen
        
        self.shouldRemove = False
        
        self.left_offset = 0
        self.top_offset = 0
        
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
            
        self.x = self.rect.left - self.left_offset
        self.y = self.rect.top - self.top_offset
        
    def update(self):
        pass

    def draw(self):
        x_diff = self.game.player.x - (self.game.map_screen.get_width() / 2)
        y_diff = self.game.player.y - (self.game.map_screen.get_height() / 2)
        rect = self.rect.move(-x_diff, -y_diff)
        self.game.map_screen.blit(self.current_image, rect)
    
    def attacked(self, source):
        pass
    
    def ranOver(self, source):
        pass