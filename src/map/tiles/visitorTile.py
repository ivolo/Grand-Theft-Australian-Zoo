from Tile import Tile

class VisitorTile(Tile):
    
    def __init__(self, image, x, y, game):
        Tile.__init__(self, image, x, y, game)
        
        self.walkable = True
        self.visible = True
        self.swimmable = False