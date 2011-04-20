'''
Created on Apr 20, 2011

@author: krakauer
'''
from game_objects.gameObject import GameObject
from player.taz import Taz

tile_size = 32

# A weak fence that can be killed by Taz when attacked
class Fence(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Fence, self).__init__(image, (x*tile_size, y*tile_size), game)
        
    def attacked(self, source):
        if isinstance(source, Taz):
            self.kill()
            
    def draw(self):
        self.screen.blit(self.image, (self.x,self.y))