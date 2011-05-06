''''
Created on Apr 28, 2011

@author: krakauer
'''
import os
from game_objects.gameObject import GameObject
from player.taz import Taz
from utils import image_util
from game_constants.client import TILE_SIZE
from pygame.examples.aliens import load_image
from game_variables import animals_freed
from map.cutscene import Cutscene

# A weak fence that can be killed by Taz when attacked
class KoalaFence(GameObject):
    
    def __init__(self, image, x, y, game):
        super(KoalaFence, self).__init__(image, (x*TILE_SIZE, y*TILE_SIZE), game)
        self.game.current_map.unjumpable_objects.add(self)
            
    def ranOver(self, source):
        self.kill()
        if "Koala" not in animals_freed:
            self.game.free_animal("Koala")
            cutscene = Cutscene(self.game, "freed_koalas", \
                                 [image_util.load_image(os.path.join("cutscenes","koala_intro.png"))], \
                                 image_util.load_sliced_sprites(210, 80, os.path.join("cutscenes","press_enter.png")));
            cutscene.fire(self.game.player)
