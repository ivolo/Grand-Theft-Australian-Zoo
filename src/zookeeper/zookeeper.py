import random

from game_objects.gameObject import GameObject
from utils.image_util import load_image
from utils.sprite_util import get_distance
from utils import image_util

tile_size = 32

class Zookeeper(GameObject):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("zookeeper.png")
        super(Zookeeper, self).__init__(image, (x*tile_size,y*tile_size), game)
        self.speed = 1
        self.game.current_map.num_zookeepers += 1
    
    def update(self):
        player = self.game.player        
        if get_distance(self, player) <= 200:
            # move away
            x = 1 if self.rect.left - player.rect.left < 0 else - 1 
            y = 1 if self.rect.top - player.rect.top < 0 else - 1
            self.move(x, y)
            
        if self.rect.colliderect(player.rect):
            self.game.reset()
            
        if self.shouldRemove:
            self.game.current_map.num_zookeepers -= 1
            self.kill()

        
    def ranOver(self, source):
        self.shouldRemove = True