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
        speed = 2
        
        attack_length = 250
        attack_delay = 200
        
        Player.__init__(self, game, x, y, image, attack_image, rect, speed, attack_length, attack_delay)
    
        self.attack_sprite = Sprite()
        self.attack_sprite.rect = image.get_rect()
    
    def attack(self):
        started = Player.attack(self)
        
        if not started:
            return
        
        self.attack_sprite.x = self.x
        self.attack_sprite.y = self.y
        
        collisions = pygame.sprite.spritecollideany(self.attack_sprite, self.game.current_map.game_objects)
        if collisions is not None:
            print "attack!", collisions
        