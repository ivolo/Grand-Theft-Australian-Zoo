import pygame

from game_objects.gameObject import GameObject
from pygame import time
from car.car import Car
from utils.sprite_util import check_collision

tile_size = 32

class Player(GameObject):
    
    def __init__(self, game, x, y, image, attack_image, unselected_images, rect, speed, attack_length, attack_delay):
        super(Player, self).__init__(image, (x*tile_size,y*tile_size), game)
        
        self.screen = game.screen
        self.rect = self.image.get_rect()
        self.speed = 1
        
        self.screen = game.screen
        
        self.attack_image = attack_image
        self.rect = rect
        self.rect.left = self.x
        self.rect.top = self.y
        self.speed = speed
    
        self.unselected_images = unselected_images
        self.last_unselected_change = time.get_ticks()
        self.unselected_change_delay = 250
        self.unselected_image = 0
        
        self.current_image = self.unselected_images[self.unselected_image]
    
        self.attack_length = attack_length
        self.attack_delay = attack_delay
        self.attack_end = 0
        self.attack_start = 0
        self.attacking = False
        
        self.isInCar = False
        
        self.inUse = False
        self.game.player_group.add(self)
    
    def newPlayer(self):
        pass
    
    def draw(self):
        if(self.isInCar):
            return
        
        super(Player, self).draw()
    
    def update(self):
        if(self.isInCar):
            return
        
        if not self.inUse:
            #update the image
            if self.last_unselected_change + self.unselected_change_delay < time.get_ticks():
                self.unselected_image += 1
                if self.unselected_image >= len(self.unselected_images):
                    self.unselected_image = 0
                self.current_image = self.unselected_images[self.unselected_image]
                self.last_unselected_change = time.get_ticks()
        
        if self.attacking:
            if self.attack_start + self.attack_length < time.get_ticks():
                self.attacking = False
                self.current_image = self.image
                self.attack_end = time.get_ticks()
                
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
        
    def collides_with_tiles(self, x, y):
        x += self.rect.left
        y += self.rect.top
        
        # check all four corners
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
            
        return True
    
    def use_ability(self):
        pass
    
    def attack(self):
        if(self.isInCar):
            return
        
        if self.attacking or time.get_ticks() < self.attack_delay + self.attack_end:
            return False
        
        self.attacking = True
        self.attack_start = time.get_ticks()
        self.current_image = self.attack_image
        return True

    # car stuff
    def move(self, x_change,  y_change):
        if(self.isInCar):
            return
        
        GameObject.move(self, x_change, y_change)
    
    def toggle_car(self):
        if not self.isInCar:
            self.get_into_car()
        else:
            self.leave_car()
    
    def get_into_car(self):
        if not self.canDriveCar:
            return
        
        if(self.isInCar):
            return;
        
        self.attack_sprite.rect.top = self.y - 5
        self.attack_sprite.rect.left = self.x - 5
        collisions = pygame.sprite.spritecollide(self.attack_sprite, self.game.current_map.game_objects, False)
        if collisions is not None:
            for collision in collisions:
                if isinstance(collision, Car):
                    self.isInCar = True
                    collision.inCar(self)
                    self.car = collision
                    self.game.current_map.game_objects.remove(self)
                    self.x = -1000
                    self.y = -1000
                    self.rect.top = -1000
                    self.rect.left = -1000
                    break;
                    
    def leave_car(self):
        if self.isInCar:
            #find some spot to put myself
            self.x = self.car.x
            self.y = self.car.y - self.rect.height - 1
            self.rect.top = self.y + self.top_offset
            self.rect.left = self.x + self.left_offset
            if (check_collision(self, self.game.current_map.game_objects) or 
                check_collision(self, self.game.current_map.unwalkable_tiles)):
                self.y = self.car.y + self.car.rect.height
                self.rect.top = self.y + self.top_offset
                self.rect.left = self.x + self.left_offset
                if (check_collision(self, self.game.current_map.game_objects) or 
                    check_collision(self, self.game.current_map.unwalkable_tiles)):
                    self.x = self.car.x - self.rect.width - 1
                    self.y = self.car.y
                    self.rect.top = self.y + self.top_offset
                    self.rect.left = self.x + self.left_offset
                    if (check_collision(self, self.game.current_map.game_objects) or 
                        check_collision(self, self.game.current_map.unwalkable_tiles)):
                        self.x = self.car.x + self.car.rect.width + self.rect.width + 1
                        self.rect.top = self.y + self.top_offset
                        self.rect.left = self.x + self.left_offset
                        if (check_collision(self, self.game.current_map.game_objects) or 
                            check_collision(self, self.game.current_map.unwalkable_tiles)):
                            # Oh well, I guess we're stuck
                            return
            
            self.car.leaveCar()
            self.isInCar = False
            self.car = None
            self.game.current_map.game_objects.add(self)
            
