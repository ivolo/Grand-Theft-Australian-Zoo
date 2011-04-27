from game_objects.gameObject import GameObject
from utils import image_util
from game_constants.client import TILE_SIZE


class Splat(GameObject):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("splat.png")
        super(Splat, self).__init__(image, (x,y), game)