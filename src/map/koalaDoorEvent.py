from utils import image_util
from specialObject.koala_door import KoalaDoor
from player.koala import Koala

class KoalaDoorEvent:
    
    def __init__(self, x, y, game):
        self.game = game
        self.door = KoalaDoor(image_util.load_image("snake_door.png"), x, y - 1, game)
    
    def fire(self, source):
        if source is self.game.player and isinstance(source, Koala):
            self.door.end(source)
            self.game.free_animal("Brown Snake")