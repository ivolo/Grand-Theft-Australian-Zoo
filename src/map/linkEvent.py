from mapEvent import MapEvent

class LinkEvent(MapEvent):
    
    def __init__(self, start_coords, end_coords, dest, game):
        self.source_x = start_coords[0]
        self.source_y = start_coords[1]
        
        self.dest_x = end_coords[0]
        self.dest_y = end_coords[1]
        
        self.dest = dest
        
        self.game = game
    
    def fire(self):
        self.game.change_maps(self.dest, self.dest_x, self.dest_y)