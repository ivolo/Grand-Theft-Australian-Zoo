from game_objects.gameObject import GameObject
from utils.image_util import load_image

tile_size = 32

class Visitor(GameObject):
    
    def __init__(self, image, x, y, game):
        
        self.game = game
        self.screen = game.screen
        

        
        self.image = load_image("visitor.png");
        self.rect = self.image.get_rect()
        super(Visitor, self).__init__((x, y))
        self.x = x * tile_size
        self.y = y * tile_size
        self.rect.left = self.x
        self.rect.top = self.y
        self.speed = 1
        
    
    def update(self):
        return
    
    def draw(self):
        self.screen.blit(self.image, (self.x,self.y))