'''
Created on Apr 30, 2011

@author: krakauer
'''
from game_objects.gameObject import GameObject
from game_constants.client import TILE_SIZE
from player.koala import Koala

# A weak fence that can be killed by Taz when attacked
class WalkableRoof(GameObject):
    
    def __init__(self, image, x, y, game):
        super(WalkableRoof, self).__init__(image, (x*TILE_SIZE, y*TILE_SIZE), game)
        self.game.current_map.high_level.add(self)

        
        
    
    

            