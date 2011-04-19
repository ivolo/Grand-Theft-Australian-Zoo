from player import Player
from utils import image_util


class Taz(Player):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("taz.png")
        rect = image.get_rect()
        speed = 2
        
        Player.__init__(self, game, x, y, image, rect, speed)