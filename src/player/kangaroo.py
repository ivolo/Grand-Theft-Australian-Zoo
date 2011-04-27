from player import Player
from utils import image_util
from pygame import time
import pygame
from pygame.sprite import Sprite
from car.car import Car

class Kangaroo(Player):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("kangaroo.png")
        
        self.init_image = image
        self.init_x = x
        self.init_y = y
        
        attack_image = image_util.load_image("taz_attack.png")
        rect = image.get_rect()
        rect.left = 5
        rect.top = 5
        rect.width = rect.width-10
        rect.height = rect.height-10
        speed = 3
        
        attack_length = 250
        attack_delay = 200
        
        Player.__init__(self, game, x, y, image, attack_image, rect, speed, attack_length, attack_delay)
    
        self.left_offset = 5
        self.top_offset = 5
    
        self.attack_sprite = Sprite()
        self.attack_sprite.rect = image.get_rect()
        self.attack_sprite.rect.width += 10
        self.attack_sprite.rect.height += 10
        
        self.canDriveCar = True
    
    def newPlayer(self):
        return Kangaroo(self.init_image, self.init_x, self.init_y, self.game)
    
    def use_ability(self):
        # jump
        # get the tile we're facing
        
        pass
    
    def attack(self):
        pass
    
    