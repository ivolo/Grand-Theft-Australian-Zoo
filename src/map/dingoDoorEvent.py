from utils import image_util
from specialObject.koala_door import KoalaDoor
from player.koala import Koala
from specialObject.dingo_door import DingoDoor

class DingoDoorEvent:
    
    def __init__(self, x, y, game):
        self.game = game
        self.door = DingoDoor(image_util.load_image("dingofence_lock.png"), x, y + 1, game)
    
    def fire(self, source):
        if source is self.game.player and self.game.hasKey:
            self.door.end(source)
            self.game.free_animal("Dingo")