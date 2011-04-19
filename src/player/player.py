from game_objects.gameObject import GameObject
from pygame import time

tile_size = 32

class Player(GameObject):
    
    def __init__(self, game, x, y, image, attack_image, rect, speed, attack_length, attack_delay):
        self.game = game
        self.screen = game.screen
        
        self.x = x * tile_size
        self.y = y * tile_size
        
        self.image = image
        self.attack_image = attack_image
        self.rect = rect
        self.speed = speed
    
        self.current_image = self.image
    
        self.attack_length = attack_length
        self.attack_delay = attack_delay
        self.attack_end = 0
        self.attack_start = 0
        self.attacking = False
    
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
        new_x = x_change * self.speed + self.x
        if new_x >= 0 and new_x < self.game.screen_dim[0] - self.rect.width:
            if self.collides_with_tiles(new_x, self.y):
                self.x = new_x
        
        # check y
        new_y = y_change * self.speed + self.y
        if new_y >= 0 and new_y < self.game.screen_dim[1] - self.rect.height:
            if self.collides_with_tiles(self.x, new_y):
                self.y = new_y
        
    def use_ability(self):
        pass
    
    def attack(self):
        if self.attacking or time.get_ticks() < self.attack_delay + self.attack_end:
            return
        
        self.attacking = True
        self.attack_start = time.get_ticks()
        self.current_image = self.attack_image