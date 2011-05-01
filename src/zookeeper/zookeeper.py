import random

from game_objects.gameObject import GameObject
from utils.image_util import load_image
from utils.sprite_util import get_distance, check_collision
from utils import image_util
from player.player import Player
from visitor.visitor import Visitor
import pygame
from game_constants.client import TILE_SIZE

tile_size = 32

class Zookeeper(GameObject):
    
    def __init__(self, image, x, y, game):
        image = image_util.load_image("zookeeper.png")
        super(Zookeeper, self).__init__(image, (x*tile_size,y*tile_size), game)
        self.speed = 1
        self.game.current_map.num_zookeepers += 1
    
    def update(self):
        player = self.game.player       
        if player.isInCar:
            if get_distance(self, player.car) <= 100:
                # move away
                x = 1 if self.rect.left - player.car.rect.left > 0 else - 1 
                y = 1 if self.rect.top - player.car.rect.top > 0 else - 1
                self.move(x, y) 
        elif get_distance(self, player) <= 200:
            # move away
            x = 1 if self.rect.left - player.rect.left < 0 else - 1 
            y = 1 if self.rect.top - player.rect.top < 0 else - 1
            self.move(x, y)
        
            rectangle = pygame.Rect(player.x, player.y, TILE_SIZE, TILE_SIZE)
            
            if self.rect.colliderect(rectangle):
                self.game.reset()
            
        if self.shouldRemove:
            self.die()

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

    def die(self):
        self.game.hud.add_zookeeper_killed()
        self.game.current_map.num_zookeepers -= 1
        self.game.current_map.add_splat(self.x, self.y)
        self.kill()
        
    def ranOver(self, source):
        self.die()