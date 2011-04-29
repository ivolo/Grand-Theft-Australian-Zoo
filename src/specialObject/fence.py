'''
Created on Apr 20, 2011

@author: krakauer
'''
from game_objects.gameObject import GameObject
from player.taz import Taz
from utils import image_util
from game_constants.client import TILE_SIZE

# A weak fence that can be killed by Taz when attacked
class Fence(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Fence, self).__init__(image, (x*TILE_SIZE, y*TILE_SIZE), game)
        
    def attacked(self, source):
        if isinstance(source, Taz):
            self.kill()
            