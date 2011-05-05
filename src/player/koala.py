from player import Player
from utils import image_util
from pygame import time
import pygame
from pygame.sprite import Sprite
from car.car import Car
from game_constants.client import TILE_SIZE
from utils.sprite_util import check_collision

class Koala(Player):
    
    def __init__(self, image, x, y, game):
        self.name = "Koala"
        
        self.init_image = image
        self.init_x = x
        self.init_y = y
        
        attack_image = image_util.load_image("koala_attack.png")
        unselected_images = image_util.load_sliced_sprites(32, 32, "koala_unselected.png")
        
        rect = image.get_rect()
        rect.left = 5
        rect.top = 5
        rect.width = rect.width-10
        rect.height = rect.height-10
        speed = 3
        
        attack_length = 250
        attack_delay = 200
        
        Player.__init__(self, game, x, y, image, attack_image, unselected_images, rect, speed, attack_length, attack_delay)
    
        self.normal_rect = self.rect
        self.normal_left_offset = self.left_offset
        self.normal_top_offset = self.top_offset
        self.climbing_rect = pygame.Rect(15,15,rect.width - 30, rect.height - 30)
        self.climbing_left_offset = 15
        self.climbing_top_offset = 15
    
        self.attack_sprite = Sprite()
        self.attack_sprite.rect = image.get_rect()
        
        self.canDriveCar = False
        self.isInTree = False
    
    def newPlayer(self):
        return Koala(self.init_image, self.init_x, self.init_y, self.game)
    
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
                
        self.game.soundUtil.LoadSound('wildcat.wav', "player")
        self.game.soundUtil.PlaySound("player")
    
    def move(self, x_change, y_change):
        if not self.isInTree:
            Player.move(self, x_change, y_change)
            return
             
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if self.rect.left < 0 or self.rect.left + self.rect.width >= self.game.current_map.width:
            self.rect = old_rect
        elif (not check_collision(self, self.game.current_map.high_level)):
            self.rect = old_rect
        
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if self.rect.top < 0 or self.rect.top + self.rect.height >= self.game.current_map.height:
            self.rect = old_rect
        elif (not check_collision(self, self.game.current_map.high_level)):
            self.rect = old_rect
            
        self.x = self.rect.left - self.left_offset
        self.y = self.rect.top - self.top_offset
        
        self.fire_tiles()
    
    def climbIntoTree(self, tree):
        if self.isInTree:
            self.rect = self.normal_rect
            self.left_offset = self.normal_left_offset
            self.top_offset = self.normal_top_offset
            self.getOutOfTree()
            return
        
        self.isInTree = True
        self.rect = self.climbing_rect
        self.left_offset = self.climbing_left_offset
        self.top_offset = self.climbing_top_offset
        self.x = tree.x
        self.y = tree.y
        self.rect.left = self.x + self.left_offset
        self.rect.top = self.y + self.top_offset

    def getOutOfTree(self):
        #find some spot to put myself
        oldx = self.x
        oldy = self.y
        self.y = oldy - TILE_SIZE
        self.rect.top = self.y + self.top_offset
        self.rect.left = self.x + self.left_offset
        if (check_collision(self, self.game.current_map.game_objects) or 
            check_collision(self, self.game.current_map.unwalkable_tiles)):
            self.y = oldy + TILE_SIZE
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if (check_collision(self, self.game.current_map.game_objects) or 
                check_collision(self, self.game.current_map.unwalkable_tiles)):
                self.x = oldx - TILE_SIZE
                self.y = oldy
                self.rect.top = self.y + self.top_offset
                self.rect.left = self.x + self.left_offset
                if (check_collision(self, self.game.current_map.game_objects) or 
                    check_collision(self, self.game.current_map.unwalkable_tiles)):
                    self.x = oldx + TILE_SIZE
                    self.rect.top = self.y + self.top_offset
                    self.rect.left = self.x + self.left_offset
                    if (check_collision(self, self.game.current_map.game_objects) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                        self.x = oldx
                        self.y = oldy
                        self.rect = self.climbing_rect
                        self.left_offset = self.climbing_left_offset
                        self.top_offset = self.climbing_top_offset
                        self.rect.top = self.y + self.top_offset
                        self.rect.left = self.x + self.left_offset
                        return
        self.isInTree = False    