from utils.image_util import *
from tiles.Tile import Tile

import os
from tiles.FloorTile import FloorTile
from tiles.WaterTile import WaterTile
from tiles.WallTile import WallTile
from visitor.visitor import Visitor
from zookeeper.zookeeper import Zookeeper
from specialObject.fance import Fence
from car.car import Car
from player.kangaroo import Kangaroo

# The dictionary describing tiles
# The form is: character : (tile image file, tile Class)
tiles = { '' : (os.path.join("tiles","grass.png"), FloorTile),
          'w': (os.path.join("tiles","water.png"), WaterTile),
          's': (os.path.join("tiles","stone_wall.png"), WallTile),
          'p': (os.path.join("tiles","path.png"), FloorTile)
        }

# The dictionary describing sprites (non-Player)
# The form is: character : (sprite image file, sprite Class)
sprites = { 'V' : (os.path.join("visitor.png"), Visitor),
            'Z' : (os.path.join("zookeeper.png"), Zookeeper),
            'F' : (os.path.join("fence.png"), Fence),
            'C' : (os.path.join("car.png"), Car),
            'K' : (os.path.join("kangaroo.png"), Kangaroo)}

loaded_sprites = {}
loaded_tiles = {}

def generateTile(key,x,y,game):#screen,gameMap):
    """
    Generates Tile object
    """
    image=getTileImages(key)
    return tiles[key][1](image,x,y,game)

def getTileImages(key):
    """
    Makes sure that we don't waste time importing new tiles every time
    """
    if not loaded_tiles.has_key(key):
        loaded_tiles[key] = load_image(tiles[key][0])

    return loaded_tiles[key]

def generateSprite(key,x,y,game):
    """
    Generates Tile object
    """
    image = getSpriteImages(key)
    return sprites[key][1](image,x,y,game)

def getSpriteImages(key):
    """
    Makes sure that we don't waste time importing new sprites every time
    """
    if not loaded_sprites.has_key(key):
        image = load_image(sprites[key][0])
        loaded_sprites[key] = image

    return loaded_sprites[key]

