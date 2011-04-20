import pygame

from game_objects.gameObject import GameObject
from pygame import time

tile_size = 32

class Player(GameObject):
    
    def __init__(self, game, x, y, image, attack_image, rect, speed, attack_length, attack_delay):
        super(Player, self).__init__(image, (x*tile_size,y*tile_size), game)
        
        self.screen = game.screen
        self.rect = self.image.get_rect()
        self.speed = 1
        
        self.screen = game.screen
        
        self.attack_image = attack_image
        self.rect = rect
        self.rect.left = self.x
        self.rect.right = self.y
        self.speed = speed
    
        self.current_image = self.image
    
        self.attack_length = attack_length
        self.attack_delay = attack_delay
        self.attack_end = 0
        self.attack_start = 0
        self.attacking = False
        super(Player, self).__init__((x * tile_size, y * tile_size))
    
    def draw(self):
        self.screen.blit(self.current_image, (self.x,self.y))
    
    def update(self):
        if self.attacking:
            if self.attack_start + self.attack_length < time.get_ticks():
                self.attacking = False
                self.current_image = self.image
                self.attack_end = time.get_ticks()
                
        self.fire_tiles()
    
    def fire_tiles(self):
        x = self.x + self.rect.left
        y = self.y + self.rect.top
        
        # check all four corners
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        self.game.current_map.fire_tile(new_tile_idx, self)
        
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        self.game.current_map.fire_tile(new_tile_idx, self)
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        self.game.current_map.fire_tile(new_tile_idx, self)
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        self.game.current_map.fire_tile(new_tile_idx, self)
    
    def collides_with_tiles(self, x, y):
        x += self.rect.left
        y += self.rect.top
        
        # check all four corners
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
            
        return True
    
    def move(self, x_change, y_change):
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if (pygame.sprite.spritecollideany(self, self.game.current_map.game_objects) or
            pygame.sprite.spritecollideany(self, self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
            
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if (pygame.sprite.spritecollideany(self, self.game.current_map.game_objects) or
            pygame.sprite.spritecollideany(self, self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
            
        self.x = self.rect.left
        self.y = self.rect.top

    def use_ability(self):
        pass
    
    def attack(self):
        if self.attacking or time.get_ticks() < self.attack_delay + self.attack_end:
            return
        
        self.attacking = True
        self.attack_start = time.get_ticks()
        self.current_image = self.attack_image