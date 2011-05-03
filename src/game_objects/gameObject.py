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
        if (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unwalkable_tiles)):
            self.fix_me()
             
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if self.rect.left < 0 or self.rect.left + self.rect.width >= self.game.current_map.width:
            self.rect = old_rect
        elif (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
        
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if self.rect.top < 0 or self.rect.top + self.rect.height >= self.game.current_map.height:
            self.rect = old_rect
        elif (check_collision(self, self.game.current_map.game_objects) or 
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
        amt = TILE_SIZE/32
        
        while(True):
            self.x = old_x + radius * amt
            self.y = old_y
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.game_objects) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    return
            
            self.x = old_x
            self.y = old_y + radius * amt
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.game_objects) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    return
            
            self.x = old_x - radius * amt
            self.y = old_y
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.game_objects) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    return
            
            self.x = old_x
            self.y = old_y - radius * amt
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.game_objects) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    return
            
            radius += 1
        
    def update(self):
        pass

    def draw(self):
        x_diff = self.game.player.x - (self.game.map_screen.get_width() / 2)
        y_diff = self.game.player.y - (self.game.map_screen.get_height() / 2)
        rect = self.rect.move(-x_diff - self.left_offset, -y_diff - self.top_offset)
        self.game.map_screen.blit(self.current_image, rect)
    
    def attacked(self, source):
        pass
    
    def ranOver(self, source):
        pass
    
    def use(self, source):
        '''
            when you want to press "Q" to
            use an object, this method is called
        '''
        pass