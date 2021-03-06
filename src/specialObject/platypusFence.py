'''
Created on Apr 29, 2011

@author: krakauer
'''
'''
Created on Apr 29, 2011

@author: krakauer
'''
from game_objects.gameObject import GameObject
from player.taz import Taz
from utils import image_util
from game_constants.client import TILE_SIZE

# A weak fence that can be killed by Taz when attacked
class PlatypusFence(GameObject):
    
    def __init__(self, image, x, y, game):
        super(PlatypusFence, self).__init__(image, (x*TILE_SIZE, y*TILE_SIZE), game)
        
    def attacked(self, source):
        if isinstance(source, Taz):
            self.game.free_animal("Platypus")
            self.kill()
            
    def ranOver(self, source):
        self.game.free_animal("Platypus")
        self.kill()
            

    