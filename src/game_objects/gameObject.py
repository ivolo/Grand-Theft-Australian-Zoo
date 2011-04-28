'''
Created on Apr 15, 2011

@author: calvin
'''
import pygame

from utils.sprite_util import check_collision
from game_constants.client import TILE_SIZE

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
        
    def fix_me(self):
        if not (check_collision(self, self.game.current_map.game_objects) or 
                check_collision(self, self.game.current_map.unwalkable_tiles)):
            return
        
        old_x = self.x
        old_y = self.y
        
        radius = 1
        while(True):
            self.x = old_x + radius * TILE_SIZE
            self.y = old_y
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if not (check_collision(self, self.game.current_map.game_objects) or 
                    check_collision(self, self.game.current_map.unwalkable_tiles)):
                return
            
            self.x = old_x
            self.y = old_y + radius * TILE_SIZE
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if not (check_collision(self, self.game.current_map.game_objects) or 
                    check_collision(self, self.game.current_map.unwalkable_tiles)):
                return
            
            self.x = old_x - radius * TILE_SIZE
            self.y = old_y
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if not (check_collision(self, self.game.current_map.game_objects) or 
                    check_collision(self, self.game.current_map.unwalkable_tiles)):
                return
            
            self.x = old_x
            self.y = old_y - radius * TILE_SIZE
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if not (check_collision(self, self.game.current_map.game_objects) or 
                    check_collision(self, self.game.current_map.unwalkable_tiles)):
                return
        
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