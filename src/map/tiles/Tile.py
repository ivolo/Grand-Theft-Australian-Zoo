from game_objects.gameObject import GameObject

tile_size = 32

class Tile(GameObject):
    
    walkable = False
    visible = False
    swimmable = False
    
    def __init__(self, image, x, y, game):
        
        self.image = image
        self.x = x
        self.y = y
        self.map_x = x * tile_size
        self.map_y = y * tile_size
        self.game = game
        self.screen = self.game.screen
        super(Tile, self).__init__(image, (x, y), game)
        self.rect.left = self.map_x
        self.rect.top = self.map_y
        
    def draw(self):
        self.screen.blit(self.image, (self.map_x, self.map_y))