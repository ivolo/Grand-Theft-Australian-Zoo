'''
Created on Apr 20, 2011

@author: krakauer
'''
from game_objects.gameObject import GameObject
from player.taz import Taz
from utils import image_util

tile_size = 32

# A weak fence that can be killed by Taz when attacked
class Fence(GameObject):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("fence.png")
        super(Fence, self).__init__(image, (x*tile_size, y*tile_size), game)
        
    def attacked(self, source):
        if isinstance(source, Taz):
            self.kill()
            