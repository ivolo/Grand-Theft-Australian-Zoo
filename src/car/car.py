'''
Created on Apr 20, 2011

@author: krakauer
'''
from game_objects.gameObject import GameObject

tile_size = 32

class Car(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Car, self).__init__(image, (x*tile_size,y*tile_size), game)
        self.speed = 6
        
        self.forward_inertia = 0
        self.side_inertia = 0
        
    def move(self, x_change, y_change):
        # do some fancy physics stuff
        pass
    
    def update(self):
        # check collisions with objects
        pass