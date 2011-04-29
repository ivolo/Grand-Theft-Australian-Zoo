from player import Player
from utils import image_util
from pygame import time
import pygame
from pygame.sprite import Sprite
from car.car import Car
from utils.sprite_util import check_collision
from game_constants.client import TILE_SIZE
from visitor.visitor import Visitor

class Platypus(Player):
    
    def __init__(self, image, x, y, game):
        self.name = "Platypus"
        
        image = image_util.load_image("platypus.png")
        
        self.init_image = image
        self.init_x = x
        self.init_y = y
        
        attack_image = image_util.load_image("platypus_attack.png")
        unselected_images = image_util.load_sliced_sprites(32, 32, "platypus_unselected.png")
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
        
        self.canDriveCar = False
    
    def newPlayer(self):
        return Platypus(None, self.init_x, self.init_y, self.game)
    
    def move(self, x_change, y_change):
        if (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unswimmable_and_unwalkable_tiles)):
            self.fix_me()
             
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unswimmable_and_unwalkable_tiles)):
            self.rect = old_rect
            
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unswimmable_and_unwalkable_tiles)):
            self.rect = old_rect
            
        self.x = self.rect.left - self.left_offset
        self.y = self.rect.top - self.top_offset
        
    def attack(self):
        started = Player.attack(self)
        
        if not started:
            return
        
        self.attack_sprite.rect.top = self.y - 5
        self.attack_sprite.rect.left = self.x - 5
        
        collisions = pygame.sprite.spritecollide(self.attack_sprite, self.game.current_map.game_objects, False)
        if collisions is not None:
            for collision in collisions:
                collision.attacked(self)
    
    