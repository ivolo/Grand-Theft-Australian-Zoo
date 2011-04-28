from player import Player
from utils import image_util
from pygame import time
import pygame
from pygame.sprite import Sprite
from car.car import Car
from utils.sprite_util import check_collision
from game_constants.client import TILE_SIZE
from visitor.visitor import Visitor

class Kangaroo(Player):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("kangaroo.png")
        
        self.init_image = image
        self.init_x = x
        self.init_y = y
        
        attack_image = image_util.load_image("taz_attack.png")
        unselected_images = image_util.load_sliced_sprites(32, 32, "kangaroo_unselected.png")
        rect = image.get_rect()
        rect.left = 5
        rect.top = 5
        rect.width = rect.width-10
        rect.height = rect.height-10
        speed = 3
        
        attack_length = 250
        attack_delay = 200
        
        Player.__init__(self, game, x, y, image, attack_image, unselected_images, rect, speed, attack_length, attack_delay)
    
        self.left_offset = 5
        self.top_offset = 5
    
        self.attack_sprite = Sprite()
        self.attack_sprite.rect = image.get_rect()
        self.attack_sprite.rect.width += 10
        self.attack_sprite.rect.height += 10
        
        self.canDriveCar = True
    
        # jump
        self.jump_images = image_util.load_sliced_sprites(32, 32, "kangaroo_jump.png")
        self.jump_init_time = 50
        self.jump_time = 500
        self.is_jumping = False
        self.last_jump = -self.jump_time
    
    def newPlayer(self):
        return Kangaroo(self.init_x, self.init_y, self.game)
    
    def use_ability(self):
        pass
    
    def update(self):
        Player.update(self)
        
        if self.is_jumping and self.last_jump + self.jump_time < time.get_ticks():
            self.is_jumping = False
            self.land()
    
    def draw(self):
        if not self.is_jumping:
            Player.draw(self)
            return
        
        if time.get_ticks() < self.last_jump + self.jump_init_time:
            self.current_image = self.jump_images[0]
        elif time.get_ticks() < self.last_jump + self.jump_time - self.jump_init_time:
            self.current_image = self.jump_images[1]
        elif time.get_ticks() < self.last_jump + self.jump_time:
            self.current_image = self.jump_images[2]

        Player.draw(self)
    
    def move(self, x_change, y_change):
        if not self.is_jumping:
            Player.move(self, x_change, y_change)
            return
        
        newx = x_change + self.x
        newy = y_change + self.y
        
        # x
        # make sure we're still on the map
        if newx < 0 or newx >= self.game.current_map.tiles_wide*32:
            newx = self.x
        
        if newy < 0 or newy >= self.game.current_map.tiles_high*32:
            newy = self.y
            
        if self.x is newx and self.y is newy:
            return
        
        print "jumping!"
        
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if check_collision(self, self.game.current_map.unjumpable_tiles):
            self.rect = old_rect
            
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if check_collision(self, self.game.current_map.unjumpable_tiles):
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
    
    def land(self):
        self.current_image = self.image
        
        collisions = pygame.sprite.spritecollide(self, self.game.current_map.game_objects, False)
        for collider in collisions:
            if isinstance(collider, Visitor):
                collider.die()
        
        if check_collision(self, self.game.current_map.unwalkable_tiles) \
            or check_collision(self, self.game.current_map.game_objects):
            self.fix_me()
            
        pass
        
    def attack(self):
        if self.is_jumping:
            return
        
        self.is_jumping = True
        self.last_jump = time.get_ticks()
    
    