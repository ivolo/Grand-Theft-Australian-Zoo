import sys,os
from tiles.Tile import Tile
import TileFactory

class Map:
    tile_size = 32   
    
    def __init__(self, name,screen,game):
        # Make the full pathnane of the map
        self.fullname = os.path.join('map', 'maps', name)

        self.gameObjects = []
        self.tiles = []
        
        self.screen=screen
        self.game=game
        
        self.events = dict()
        
        self.tiles_wide = screen.get_width()/self.tile_size
        self.tiles_high = screen.get_height()/self.tile_size
        self.num_tiles = self.tiles_wide * self.tiles_high

    def intialize(self):
        file = open(self.fullname, 'r')
        self.load_map(file)

    def fire_tile(self, index, source):
        if index in self.events:
            for event in self.events[index]:
                event.fire(source)

    def draw_tiles(self):
        for tile in self.tiles:
            tile.draw()
        
    def draw_objects(self):
        for obj in self.gameObjects:
            obj.draw()

    # Load the map from the text file
    # Maps are comma separated value files
    # where each value is an index into the array found
    # in TileFactory.py.
    def load_map(self, file):
        lines = file.readlines()
        
        # Load the tile map
        for y in xrange(0, self.tiles_high):
            line = lines[y]
            
            parsed_comments = line.split('#');
            
            line_tiles = parsed_comments[0].replace(' ','').replace('\n','').split(',')
            
            x = 0
            for key in line_tiles:
                self.tiles.append( TileFactory.generateTile(key,x,y,self.game) )
                x += 1
               
        index = self.tiles_high 
        while lines[index] is "\n":
            index += 1
            
        # Load the sprite map
        for y in xrange(index, self.tiles_high + index):
            line = lines[y]
            
            parsed_comments = line.split('#');
            
            line_tiles = parsed_comments[0].replace(' ','').replace('\n','').split(',')
            
            x = 0
            for key in line_tiles:
                if key is not None and key is not '':
                    self.gameObjects.append( TileFactory.generateSprite(key,x,y - index,self.game) )
                x += 1
        
        # special commands        
        index = self.tiles_high 
        while lines[index] is "\n":
            index += 1
            
        
