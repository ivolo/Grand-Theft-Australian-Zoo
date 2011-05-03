from game_objects.gameObject import GameObject
from utils.image_util import load_image
from utils.sprite_util import get_distance
from utils import image_util
from splat import Splat
import pygame
from player.player import Player
import random

tile_size = 32

directions = [1] + ([0] * 4)  + [-1]
MOVEMENT_TIME = 40

class Visitor(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Visitor, self).__init__(image, (x*tile_size,y*tile_size), game)
        self.speed = 2
        self.game.current_map.num_visitors += 1
        self.reset_move()
        self.ticks = MOVEMENT_TIME
    
    def update(self):
        player = self.game.player
        
        if player.isInCar:
            if get_distance(self, player.car) <= 100:
                # move away
                x = 1 if self.rect.left - player.car.rect.left > 0 else - 1 
                y = 1 if self.rect.top - player.car.rect.top > 0 else - 1
                self.move(x, y)
        
        elif get_distance(self, player) <= 100:
            # move away
            x = 1 if self.rect.left - player.rect.left > 0 else - 1 
            y = 1 if self.rect.top - player.rect.top > 0 else - 1
            self.move(x, y)
        
        else:
            self.ticks -= 1
            if self.ticks == 0:
                self.reset_move()
            x, y = self.heading
            self.move(x, y) 
            
        if self.shouldRemove:
            self.die()
    
    def reset_move(self):
        self.ticks = MOVEMENT_TIME
        self.heading = random.choice(directions), random.choice(directions)
    
    def check_collision(self, group):
        collisions = pygame.sprite.spritecollide(self, group, False)
        for collider in collisions:
            if not isinstance(collider, Visitor) and not isinstance(collider, Player):
                return True
        
        return False
    
    def move(self, x_change, y_change):
        if (self.check_collision(self.game.current_map.game_objects) or 
            self.check_collision(self.game.current_map.unwalkable_tiles)):
            self.fix_me()
             
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if self.rect.left < 0 or self.rect.left + self.rect.width >= self.game.current_map.width:
            self.rect = old_rect
        elif (self.check_collision(self.game.current_map.game_objects) or 
            self.check_collision(self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
        
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if self.rect.top < 0 or self.rect.top + self.rect.height >= self.game.current_map.height:
            self.rect = old_rect
        elif (self.check_collision(self.game.current_map.game_objects) or 
            self.check_collision(self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
            
        self.x = self.rect.left - self.left_offset
        self.y = self.rect.top - self.top_offset
    
    def die(self):
        self.game.hud.add_visitor_killed()
        self.game.current_map.num_visitors -= 1
        self.game.current_map.add_splat(self.x, self.y)
        self.kill()
        
    def attacked(self, source):
        self.shouldRemove = True
        
    def ranOver(self, source):
        self.die()