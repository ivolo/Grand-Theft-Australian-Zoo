from game_objects.gameObject import GameObject
from utils.image_util import load_image

tile_size = 32

class Visitor(GameObject):
    
    def __init__(self, image, x, y, game):

        self.game = game
        self.screen = game.screen
        
        super(Visitor, self).__init__(image, (x*tile_size,y*tile_size), game)

        self.screen = game.screen
        self.rect = self.image.get_rect()
        self.x = x * tile_size
        self.y = y * tile_size
        self.rect.left = self.x
        self.rect.top = self.y
        self.speed = 1
        
    
    def update(self):
        if self.shouldRemove:
            self.kill()
    
    def draw(self):
        self.screen.blit(self.image, (self.x,self.y))
        
    def attacked(self, source):
        self.shouldRemove = True