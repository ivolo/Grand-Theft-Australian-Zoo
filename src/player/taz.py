from player import Player
from utils import image_util
from pygame import time
import pygame
from pygame.sprite import Sprite

class Taz(Player):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("taz.png")
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
        