''''
Created on Apr 28, 2011

@author: krakauer
'''
from game_objects.gameObject import GameObject
from player.taz import Taz
from utils import image_util
from game_constants.client import TILE_SIZE
from pygame.examples.aliens import load_image
from game_variables import animals_freed

# A weak fence that can be killed by Taz when attacked
class KoalaFence(GameObject):
    
    def __init__(self, image, x, y, game):
        super(KoalaFence, self).__init__(image, (x*TILE_SIZE, y*TILE_SIZE), game)
        self.game.current_map.unjumpable_objects.add(self)
        
    def attacked(self, source):
        if isinstance(source, Taz):
            self.game.free_animal("Koala")
            self.kill()
            
    def ranOver(self, source):
        self.game.free_animal("Koala")
        self.kill()
