from Tile import Tile

class WallTile(Tile):
    
    def __init__(self, image, x, y, game):
        Tile.__init__(self, image, x, y, game)
        
        self.walkable = False
        self.visible = False
        self.swimmable = False