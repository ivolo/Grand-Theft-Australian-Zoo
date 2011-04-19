from game_objects.gameObject import GameObject

tile_size = 32

class Player(GameObject):
    
    def __init__(self, game, x, y, image, rect, speed):
        self.game = game
        self.screen = game.screen
        
        self.x = x * tile_size
        self.y = y * tile_size
        
        self.image = image
        self.rect = rect
        self.speed = speed
    
    def draw(self):
        self.screen.blit(self.image, (self.x,self.y))
    
    def update(self):
        pass
    
    def collides_with_tiles(self, x, y):
        # check all four corners
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = y/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + x/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
        
        new_tile_idx = (y+self.rect.height)/self.game.current_map.tile_size * self.game.current_map.tiles_wide \
                           + (x+self.rect.width)/self.game.current_map.tile_size
        if not self.game.current_map.tiles[new_tile_idx].walkable:
            return False
            
        return True
    
    def move(self, x_change, y_change):
        # check x
        new_x = x_change * self.speed + self.x
        if new_x >= 0 and new_x < self.game.screen_dim[0] - self.rect.width:
            if self.collides_with_tiles(new_x, self.y):
                self.x = new_x
        
        # check y
        new_y = y_change * self.speed + self.y
        if new_y >= 0 and new_y < self.game.screen_dim[1] - self.rect.height:
            if self.collides_with_tiles(self.x, new_y):
                self.y = new_y
        
    def use_ability(self):
        raise NotImplementedError();
    
    def attack(self):
        raise NotImplementedError();