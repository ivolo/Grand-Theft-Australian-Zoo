from game_objects.gameObject import GameObject
from utils.image_util import load_image

tile_size = 32

class Zookeeper(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Zookeeper, self).__init__(image, (x*tile_size,y*tile_size), game)
        
        self.screen = game.screen
        self.rect = self.image.get_rect()
        self.speed = 1
    
    def update(self):
        return
    
    def draw(self):
        self.screen.blit(self.image, (self.x,self.y))