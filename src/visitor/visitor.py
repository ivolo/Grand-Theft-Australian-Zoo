from game_objects.gameObject import GameObject
from utils.image_util import load_image
from utils.sprite_util import get_distance

tile_size = 32

class Visitor(GameObject):
    
    def __init__(self, image, x, y, game):
        super(Visitor, self).__init__(image, (x*tile_size,y*tile_size), game)
        self.speed = 2
        
    
    def update(self):
        player = self.game.player
        if get_distance(self, player) <= 100:
            # move away
            x = 1 if self.rect.left - player.rect.left > 0 else - 1 
            y = 1 if self.rect.top - player.rect.top > 0 else - 1
            self.move(x, y)
            
        if self.shouldRemove:
            self.kill()
    
    def draw(self):
        self.screen.blit(self.image, (self.x,self.y))
        
    def attacked(self, source):
        self.shouldRemove = True
        
    def ranOver(self, source):
        self.shouldRemove = True