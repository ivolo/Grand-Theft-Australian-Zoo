from Tile import Tile

class WaterTile(Tile):
    
    def __init__(self, image, x, y, game):
        Tile.__init__(self, image, x, y, game)
        
        self.walkable = False
        self.visible = True
        self.swimmable = True