from mapEvent import MapEvent

class LinkEvent(MapEvent):
    
    def __init__(self, start_coords, end_coords, dest, game):
        self.source_x = int(start_coords[0])
        self.source_y = int(start_coords[1])
        
        self.dest_x = int(end_coords[0])
        self.dest_y = int(end_coords[1])
        
        self.dest = dest
        
        self.game = game
    
    def fire(self, source):
        if source is self.game.player or source is self.game.player.car:
            self.game.change_maps(self.dest, self.dest_x, self.dest_y)
            return False
        return True