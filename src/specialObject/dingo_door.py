'''
Created on Apr 20, 2011

@author: krakauer
'''
import os
from game_objects.gameObject import GameObject
from player.taz import Taz
from utils import image_util
from game_constants.client import TILE_SIZE
from map.cutscene import Cutscene

# A weak fence that can be killed by Taz when attacked
class DingoDoor(GameObject):
    
    def __init__(self, image, x, y, game):
        super(DingoDoor, self).__init__(image, (x*TILE_SIZE, y*TILE_SIZE), game)
        self.cutscene = Cutscene(self.game, "freed dingos", \
                                 [image_util.load_image(os.path.join("cutscenes","dingo_free.png"))], \
                                 image_util.load_sliced_sprites(210, 80, os.path.join("cutscenes","press_enter.png")));
        self.game.current_map.game_objects.add(self)
        
    def end(self, source):
        self.kill()
        self.cutscene.fire(source)
        self.game.free_animal("Dingo")
            