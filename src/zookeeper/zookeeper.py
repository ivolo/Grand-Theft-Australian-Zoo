import random

from game_objects.gameObject import GameObject
from utils.image_util import load_image

tile_size = 32

class Zookeeper(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Zookeeper, self).__init__(image, (x*tile_size,y*tile_size), game)
        self.speed = 1
    
    def update(self):

        deltas = [-1, 0, 1]
        dx = random.choice(deltas)
        dy = random.choice(deltas)
        self.move(dx, dy)
    
    def draw(self):
        self.screen.blit(self.image, (self.x,self.y))