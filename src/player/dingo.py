from player import Player
from utils import image_util
from pygame import time
import pygame
from pygame.sprite import Sprite
from car.car import Car

class Dingo(Player):
    
    def __init__(self, image, x, y, game):
        self.name = "Dingo"
        
        self.init_image = image_util.load_image("dingo.png")
        self.init_x = x
        self.init_y = y
        
        image = image_util.load_image("dingo.png")
        attack_image = image_util.load_image("dingo_attack.png")
        
        unselected_images = image_util.load_sliced_sprites(32, 32, "dingo_unselected.png")
        
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
        self.rect.width = 32 - self.left_offset * 2
        self.rect.height = self.rect.width
    
        self.attack_sprite = Sprite()
        self.attack_sprite.rect = image.get_rect()
        #self.attack_sprite.rect.width += 10
        #self.attack_sprite.rect.height += 10
        
        self.canDriveCar = False
    
    def newPlayer(self):
        return Dingo(self.init_image, self.init_x, self.init_y, self.game)
    
    def attack(self):
        started = Player.attack(self)
        
        if not started:
            return
        
        self.attack_sprite.rect.top = self.y
        self.attack_sprite.rect.left = self.x
        
        collisions = pygame.sprite.spritecollide(self.attack_sprite, self.game.current_map.game_objects, False)
        if collisions is not None:
            for collision in collisions:
                collision.attacked(self)
        