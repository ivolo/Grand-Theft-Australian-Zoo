from mapEvent import MapEvent
from game_variables import animals_freed
from game_constants.client import TILE_SIZE
from dialogEvent import DialogEvent

class PushbackLinkEvent(MapEvent):
    
    def __init__(self, start_coords, end_coords, dest, game):
        self.source_x = int(start_coords[0])
        self.source_y = int(start_coords[1])
        
        self.dest_x = int(end_coords[0])
        self.dest_y = int(end_coords[1])
        
        self.dest = dest
        
        self.game = game
    
    def fire(self, source):
        if source is self.game.player or source is self.game.player.car:
            if len(animals_freed) == 5:
                self.game.change_maps(self.dest, self.dest_x, self.dest_y)
            else:
                self.player.y -= TILE_SIZE
                self.player.rect.top = self.player.y - self.player.top_offset
                dialog = DialogEvent("You cannot leave until you've freed all the animals!", self.game)
                dialog.fire()
            return False
        return True