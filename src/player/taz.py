from player.Player import Player
from utils import image_util


class Taz(Player):
    
    def __init__(self, game, x, y):
        self.image = image_util.load_image("taz.png")
        self.rect = self.image.get_rect()
        self.speed = 2
        
        Player.__init__(self, game, x, y, self.image, self.rect, self.speed)
        
    