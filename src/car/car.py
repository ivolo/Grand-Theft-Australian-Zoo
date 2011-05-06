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
from map.linkEvent import LinkEvent
from visitor.visitor import Visitor
from zookeeper.zookeeper import Zookeeper

tile_size = 32

class Car(GameObject):
    
    def __init__(self, image, x, y, game):
        self.init_x = x
        self.init_y = y
        self.init_image = None
        
        self.images = image_util.load_sliced_sprites(32, 64, "red_car.png")
        
        super(Car, self).__init__(self.images[0], (x*tile_size,y*tile_size), game)
        
        self.current_image = self.images[0]
        
        self.speed = 1
        
        self.max_speed = 6
        
        self.forward_speed = 0
        self.side_speed = 0
        
        self.max_forward_acceleration = .5
        self.max_side_acceleration = .5
        
        self.forward_acceleration = 0
        self.side_acceleration = 0
        
        self.direction = UP
        
        self.start_time = pygame.time.get_ticks()
        
        self.driver = None
        
        self.driving = False
        
        self.health = 30
        self.damage = 0
        self.damage_index = 0
        self.first_damage_point = 10
        self.second_damage_point = 20
        self.third_damage_point = 25
        self.drag = 0.2
        
    def newCar(self):
        return Car(self.init_image, self.init_x, self.init_y, self.game)
    
    def inCar(self, source):
        self.driver = source
        self.driving = True
        self.game.soundUtil.LoadSound('engine.wav', "car")
        self.game.soundUtil.PlaySound("car")
        self.start_time = pygame.time.get_ticks()
        
    def leaveCar(self):
        self.driving = None
        self.driver = None
        self.game.soundUtil.LoadSound('cardoorshut.wav', "car")
        self.game.soundUtil.PlaySound("car")
        
    def move(self, x_change, y_change):
        new_damage = 0
        
        # check x
        old_rect = self.rect
        delta_x = x_change * self.speed
        self.rect = self.rect.move(delta_x, 0)
        if (check_collision(self, self.game.current_map.unwalkable_tiles)):
            new_damage = .1
            self.rect = old_rect
            self.side_speed = -self.side_speed
            
        old_rect = self.rect
        delta_y = y_change * self.speed
        self.rect = self.rect.move(0, delta_y)
        if (check_collision(self, self.game.current_map.unwalkable_tiles)):
            new_damage = .1
            self.rect = old_rect
            self.forward_speed = -self.forward_speed
            
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
        
        self.damage += new_damage
    
        if (pygame.time.get_ticks() > (self.start_time + 1600)) and self.driving and self.driver:
                self.game.soundUtil.LoadSound('idle.wav', "car")
                self.game.soundUtil.PlaySound("car")
    
    def fix_me(self):
        if not (check_collision(self, self.game.current_map.not_player) or 
                check_collision(self, self.game.current_map.unwalkable_tiles)):
            return
        
        old_x = self.x
        old_y = self.y
        
        radius = 1
        amt = TILE_SIZE/32
        
        while(True):
            # Checks Right, Left, Top, Bottom
            self.x = old_x + radius * amt
            self.y = old_y
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.not_player) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    #self.side_speed = -self.side_speed
                    #self.side_acceleration = -self.side_acceleration
                    return
            
            self.x = old_x
            self.y = old_y + radius * amt
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.not_player) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    #self.side_speed = -self.side_speed
                    #self.side_acceleration = -self.side_acceleration
                    return
            
            self.x = old_x - radius * amt
            self.y = old_y
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.not_player) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    #self.foward_speed = -self.forward_speed
                    #self.forward_acceleration = -self.forward_acceleration
                    return
            
            self.x = old_x
            self.y = old_y - radius * amt
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if self.rect.left >= 0 and self.rect.left + self.rect.width < self.game.current_map.width and \
                self.rect.top >= 0 and self.rect.top + self.rect.height < self.game.current_map.height:
                if not (check_collision(self, self.game.current_map.not_player) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                    #self.foward_speed = -self.forward_speed
                    #self.forward_acceleration = -self.forward_acceleration
                    return
            
            radius += 1

    def ranOver(self, source):
        self.damage += 1
        
    def update(self):
        if self.damage >= self.health:
            if self.driver:
                self.driver.x = self.rect.left
                self.driver.y = self.rect.top
                self.driver.rect.left = self.rect.left
                self.driver.rect.top = self.rect.top
                self.driver.isInCar = False
                self.driver.car = None
                self.game.current_map.game_objects.add(self.driver)
            self.kill()
        
        if self.damage >= self.first_damage_point:
            self.damage_index = 1
        if self.damage >= self.second_damage_point:
            self.damage_index = 2
        if self.damage >= self.third_damage_point:
            self.damage_index = 3
        
        
        if not self.driving:
            if(self.forward_speed == 0 and self.side_speed == 0):
                return

            if self.forward_speed > 0:
                self.forward_speed = max(0, self.forward_speed - self.drag)
            elif self.forward_speed < 0:
                self.forward_speed = min(0, self.forward_speed + self.drag)
        
            if self.side_speed > 0:
                self.side_speed = max(0, self.side_speed - self.drag)
            elif self.side_speed < 0:
                self.side_speed = min(0, self.side_speed + self.drag)
                
            #self.rect.top += self.y
            #self.rect.left += self.x
            
            self.move(self.side_speed, self.forward_speed)
            return
        
        
        self.handle_input()
        
        if self.forward_speed > 0:
            self.forward_speed = max(0, self.forward_speed - self.drag)
        elif self.forward_speed < 0:
            self.forward_speed = min(0, self.forward_speed + self.drag)
        
        if self.side_speed > 0:
            self.side_speed = max(0, self.side_speed - self.drag)
        elif self.side_speed < 0:
            self.side_speed = min(0, self.side_speed + self.drag)
                
        self.forward_speed = min( self.forward_speed + self.forward_acceleration, self.max_speed)
        self.forward_speed = max( self.forward_speed, -self.max_speed)
        self.side_speed = min( self.side_speed + self.side_acceleration, self.max_speed)
        self.side_speed = max( self.side_speed, -self.max_speed)
        
        if(abs(self.side_acceleration) > abs(self.forward_acceleration)):
            if(self.side_acceleration > 0):
                self.current_image = pygame.transform.rotate(self.images[self.damage_index], -90)
                self.direction = RIGHT
            else:
                self.current_image = pygame.transform.rotate(self.images[self.damage_index], 90)
                self.direction = LEFT
        elif(abs(self.side_acceleration) < abs(self.forward_acceleration)):
            if(self.forward_acceleration > 0):
                self.current_image = pygame.transform.rotate(self.images[self.damage_index], 180)
                self.direction = DOWN
            else:
                self.current_image = self.images[self.damage_index]
                self.direction = UP
        self.rect = self.current_image.get_rect()
        self.rect.top += self.y
        self.rect.left += self.x
        
        self.move(self.side_speed, self.forward_speed)
        
        collisions = pygame.sprite.spritecollide(self, self.game.current_map.game_objects, False)
        self.fix_me()
        if collisions is not None:
            for collision in collisions:
                if collision is not self:
                    collision.ranOver(self)
        
        self.fire_tiles()
        
    def fire_tiles(self):
        x = self.x + self.left_offset
        y = self.y + self.top_offset
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        do_continue = self.game.current_map.fire_tile(new_tile_idx, self)
        if not do_continue:
            return
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        do_continue = self.game.current_map.fire_tile(new_tile_idx, self)
        if not do_continue:
            return
        
        # check all four corners
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        do_continue = self.game.current_map.fire_tile(new_tile_idx, self)
        if not do_continue:
            return
        
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        do_continue = self.game.current_map.fire_tile(new_tile_idx, self)
        if not do_continue:
            return
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if(keys[K_s] or keys[K_DOWN]):
            self.forward_acceleration = min(self.max_forward_acceleration, self.forward_acceleration + .1)
        elif self.forward_acceleration > 0:
            self.forward_acceleration = max(0, self.forward_acceleration - .05)
    
        if(keys[K_w] or keys[K_UP]):
            self.forward_acceleration = max(-self.max_forward_acceleration, self.forward_acceleration - .1)
        elif self.forward_acceleration < 0:
            self.forward_acceleration = min(0, self.forward_acceleration + .05)
        
        if(keys[K_a] or keys[K_LEFT]):
            self.side_acceleration = max(-self.max_side_acceleration, self.side_acceleration - .1)
        elif self.side_acceleration < 0:
            self.side_acceleration = min(0, self.side_acceleration + .05)
           
        if(keys[K_d] or keys[K_RIGHT]):
            self.side_acceleration = min(self.max_side_acceleration, self.side_acceleration + .1)
        elif self.side_acceleration > 0:
            self.side_acceleration = max(0, self.side_acceleration - .05)
            
    def use(self, source):
        if not self.driving and source.canDriveCar:
            source.isInCar = True
            self.inCar(source)
            source.car = self
            self.game.current_map.game_objects.remove(source)

    def avoidMapLinks(self):
        x = self.x - 1
        y = self.y - 1
        
        index = int((y + self.current_image.get_height())/32)*self.game.current_map.tiles_wide + int(x/32)
        if index in self.game.current_map.events:
            if isinstance(self.game.current_map.events[index], LinkEvent):
                self.y -= TILE_SIZE
                self.rect.top -= TILE_SIZE
                y = self.y
        index = int((y + self.current_image.get_height())/32)*self.game.current_map.tiles_wide + int((x + self.current_image.get_width())/32)
        if index in self.game.current_map.events:
            if isinstance(self.game.current_map.events[index], LinkEvent):
                self.y -= TILE_SIZE
                self.rect.top -= TILE_SIZE
                y = self.y
                
        index = int(y/32)*self.game.current_map.tiles_wide + int(x/32)
        if index in self.game.current_map.events:
            if isinstance(self.game.current_map.events[index], LinkEvent):
                self.x += TILE_SIZE
                self.rect.top += TILE_SIZE
                x = self.x
                
        index = int((y + self.current_image.get_height())/32)*self.game.current_map.tiles_wide + int(x/32)
        if index in self.game.current_map.events:
            if isinstance(self.game.current_map.events[index], LinkEvent):
                self.x += TILE_SIZE
                self.rect.top += TILE_SIZE
                x = self.x
