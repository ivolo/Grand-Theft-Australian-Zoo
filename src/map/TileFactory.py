from utils.image_util import *
from tiles.Tile import Tile

import os
from tiles.FloorTile import FloorTile
from tiles.WaterTile import WaterTile
from tiles.WallTile import WallTile
from visitor.visitor import Visitor
from zookeeper.zookeeper import Zookeeper
from specialObject.fence import Fence
from car.car import Car
from player.kangaroo import Kangaroo
from tiles.visitorTile import VisitorTile
from player.taz import Taz
from specialObject.kangarooFence import KangarooFence
from specialObject.tazFence import TazFence
from specialObject.brokenTazFence import BrokenTazFence
from player.platypus import Platypus

# The dictionary describing tiles
# The form is: character : (tile image file, tile Class)
tiles = { '' : (os.path.join("tiles","grass.png"), FloorTile),
          'W': (os.path.join("tiles","water.png"), WaterTile),
          
          'q': (os.path.join("tiles","tallwall_UL.png"), WallTile),
          'w': (os.path.join("tiles","tallwall_horizontal.png"), WallTile),
          'e': (os.path.join("tiles","tallwall_UR.png"), WallTile),
          'd': (os.path.join("tiles","tallwall_LR.png"), WallTile),
          's': (os.path.join("tiles","tallwall_verticle.png"), WallTile),
          'a': (os.path.join("tiles","tallwall_LL.png"), WallTile),
          
          'p': (os.path.join("tiles","path.png"), VisitorTile)
        }

# The dictionary describing sprites (non-Player)
# The form is: character : (sprite image file, sprite Class)
sprites = { 'V' : (os.path.join("tourist.png"), Visitor),
            'V2' : (os.path.join("tourist2.png"), Visitor),
            'V3' : (os.path.join("tourist3.png"), Visitor),
            'Z' : (os.path.join("zookeeper.png"), Zookeeper),
            
            'F' : (os.path.join("fence.png"), Fence),
            'I' : (os.path.join("fence_verticle_left.png"), Fence),
            'U' : (os.path.join("fence_verticle_right.png"), Fence),
            'R' : (os.path.join("fence_LR.png"), Fence),
            'L' : (os.path.join("fence_LL.png"), Fence),
            'G' : (os.path.join("fence_UR.png"), Fence),
            'H' : (os.path.join("fence_UL.png"), Fence),
            
            
            'k' : (os.path.join("kangaroo_fence.png"), KangarooFence),
            'r' : (os.path.join("kangaroo_fence_LR.png"), KangarooFence),
            'l' : (os.path.join("kangaroo_fence_LL.png"), KangarooFence),
            'v' : (os.path.join("kangaroo_fence_verticle_left.png"), KangarooFence),
            'u' : (os.path.join("kangaroo_fence_verticle_right.png"), KangarooFence),
            
            'q' : (os.path.join("shortwall_UL.png"), TazFence),
            'w' : (os.path.join("shortwall_top.png"), TazFence),
            'e' : (os.path.join("shortwall_UR.png"), TazFence),
            'd' : (os.path.join("shortwall_verticle_right.png"), TazFence),
            'c' : (os.path.join("shortwall_LR.png"), TazFence),
            'x' : (os.path.join("shortwall.png"), TazFence),
            'z' : (os.path.join("shortwall_LL.png"), TazFence),
            'a' : (os.path.join("shortwall_verticle_left.png"), TazFence),
            's' : (os.path.join("shortwall_destroyed.png"), BrokenTazFence),
            
            'C' : (os.path.join("cart.png"), Car),
            'K' : (os.path.join("kangaroo.png"), Kangaroo),
            'T' : (os.path.join("taz.png"), Taz),
            'P' : (os.path.join("platypus.png"), Platypus)}

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
    return sprites[key][1](image, x,y,game)

def getSpriteImages(key):
    """
    Makes sure that we don't waste time importing new sprites every time
    """
    if not loaded_sprites.has_key(key):
        image = load_image(sprites[key][0])
        loaded_sprites[key] = image

    return loaded_sprites[key]

