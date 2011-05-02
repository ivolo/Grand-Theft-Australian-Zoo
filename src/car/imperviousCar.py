'''
Created on Apr 20, 2011

@author: krakauer
'''
import pygame
from pygame.locals import *

from game_objects.gameObject import GameObject
from utils.sprite_util import check_collision
from utils import image_util
from game_constants.client import *

tile_size = 32

class ImperviousCar(GameObject):
    
    def __init__(self, image, x, y, game):
        self.image = image
        
        super(ImperviousCar, self).__init__(self.image, (x*tile_size,y*tile_size), game)
        
        self.current_image = self.image
        
        self.speed = 1
        
        self.max_speed = 6
        
        self.forward_speed = 0
        self.side_speed = 0
        
        self.max_forward_acceleration = .5
        self.max_side_acceleration = .5
        
        self.forward_acceleration = 0
        self.side_acceleration = 0
        
        self.direction = UP
        
        self.driver = None
        
        self.driving = False
        
    def inCar(self, source):
        self.driver = source
        self.driving = True
        
    def leaveCar(self):
        self.driving = None
        self.driver = None
        
    def move(self, x_change, y_change):
        
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if (check_collision(self, self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
            
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if (check_collision(self, self.game.current_map.unwalkable_tiles)):
            self.rect = old_rect
            
        self.x = self.rect.left - self.left_offset
        self.y = self.rect.top - self.top_offset
        if self.driver:
            self.driver.x = self.x
            self.driver.y = self.y
        
        collisions = pygame.sprite.spritecollide(self, self.game.current_map.game_objects, False)
        self.fix_me()
        if collisions is not None:
            for collision in collisions:
                if collision is not self:
                    collision.ranOver(self)
        
    def update(self):
        drag = .2
        
        if not self.driving:
            if(self.forward_speed == 0 and self.side_speed == 0):
                return

            if self.forward_speed > 0:
                self.forward_speed = max(0, self.forward_speed - drag)
            elif self.forward_speed < 0:
                self.forward_speed = min(0, self.forward_speed + drag)
        
            if self.side_speed > 0:
                self.side_speed = max(0, self.side_speed - drag)
            elif self.side_speed < 0:
                self.side_speed = min(0, self.side_speed + drag)
                
            #self.rect.top += self.y
            #self.rect.left += self.x
            
            self.move(self.side_speed, self.forward_speed)
            return
        
        # check collisions with objects
        keys = pygame.key.get_pressed()
        
        if(keys[K_s]):
            self.forward_acceleration = min(self.max_forward_acceleration, self.forward_acceleration + .1)
        elif self.forward_acceleration > 0:
            self.forward_acceleration = max(0, self.forward_acceleration - .05)
    
        if(keys[K_w]):
            self.forward_acceleration = max(-self.max_forward_acceleration, self.forward_acceleration - .1)
        elif self.forward_acceleration < 0:
            self.forward_acceleration = min(0, self.forward_acceleration + .05)
        
        if(keys[K_a]):
            self.side_acceleration = max(-self.max_side_acceleration, self.side_acceleration - .1)
        elif self.side_acceleration < 0:
            self.side_acceleration = min(0, self.side_acceleration + .05)
           
        if(keys[K_d]):
            self.side_acceleration = min(self.max_side_acceleration, self.side_acceleration + .1)
        elif self.side_acceleration > 0:
            self.side_acceleration = max(0, self.side_acceleration - .05)
        
        if self.forward_speed > 0:
            self.forward_speed = max(0, self.forward_speed - drag)
        elif self.forward_speed < 0:
            self.forward_speed = min(0, self.forward_speed + drag)
        
        if self.side_speed > 0:
            self.side_speed = max(0, self.side_speed - drag)
        elif self.side_speed < 0:
            self.side_speed = min(0, self.side_speed + drag)
                
        self.forward_speed = min( self.forward_speed + self.forward_acceleration, self.max_speed)
        self.forward_speed = max( self.forward_speed, -self.max_speed)
        self.side_speed = min( self.side_speed + self.side_acceleration, self.max_speed)
        self.side_speed = max( self.side_speed, -self.max_speed)
        
        if(abs(self.side_acceleration) > abs(self.forward_acceleration)):
            if(self.side_acceleration > 0):
                self.current_image = pygame.transform.rotate(self.image, -90)
                self.direction = RIGHT
            else:
                self.current_image = pygame.transform.rotate(self.image, 90)
                self.direction = LEFT
        elif(abs(self.side_acceleration) < abs(self.forward_acceleration)):
            if(self.forward_acceleration > 0):
                self.current_image = pygame.transform.rotate(self.image, 180)
                self.direction = DOWN
            else:
                self.current_image = self.image
                self.direction = UP
        self.rect = self.current_image.get_rect()
        self.rect.top += self.y
        self.rect.left += self.x
        
        self.move(self.side_speed, self.forward_speed)

    def use(self, source):
        if not self.driving and source.canDriveCar:
            source.isInCar = True
            self.inCar(source)
            source.car = self
            self.game.current_map.game_objects.remove(source)