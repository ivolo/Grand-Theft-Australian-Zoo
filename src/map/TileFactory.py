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
from car.police import PoliceCar
from player.kangaroo import Kangaroo
from tiles.visitorTile import VisitorTile
from player.taz import Taz
from specialObject.kangarooFence import KangarooFence
from specialObject.tazFence import TazFence
from specialObject.brokenTazFence import BrokenTazFence
from player.platypus import Platypus
from specialObject.platypusFence import PlatypusFence
from specialObject.tree import Tree
from specialObject.building import Building
from specialObject.koalaFence import KoalaFence
from player.koala import Koala
from player.dingo import Dingo
from specialObject.dingoFence import DingoFence
from specialObject.highStrongFence import HighStrongFence
from car.imperviousCar import ImperviousCar
from player.snake import Snake
from specialObject.snakeFence import SnakeFence
from specialObject.walkableRoof import WalkableRoof

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
          
          'p': (os.path.join("tiles","path.png"), VisitorTile),
          'P': (os.path.join("tiles","path.png"), FloorTile),
          
          '_': (os.path.join("tiles","indoor_floor.png"), FloorTile),
        }

# The dictionary describing sprites (non-Player)
# The form is: character : (sprite image file, sprite Class)
sprites = { 'V' : (os.path.join("tourist.png"), Visitor),
            'V2' : (os.path.join("tourist2.png"), Visitor),
            'V3' : (os.path.join("tourist3.png"), Visitor),
            'Z' : (os.path.join("zookeeper.png"), Zookeeper),
            
            'f' : (os.path.join("fence.png"), Fence),
            'F' : (os.path.join("fence.png"), PlatypusFence),
            'I' : (os.path.join("fence_verticle_left.png"), PlatypusFence),
            'U' : (os.path.join("fence_verticle_right.png"), PlatypusFence),
            'R' : (os.path.join("fence_LR.png"), PlatypusFence),
            'L' : (os.path.join("fence_LL.png"), PlatypusFence),
            'G' : (os.path.join("fence_UR.png"), PlatypusFence),
            'H' : (os.path.join("fence_UL.png"), PlatypusFence),
            
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
            
            '-1' : (os.path.join("koala_fence_LL.png"), KoalaFence),
            '0' : (os.path.join("koala_fence_LR.png"), KoalaFence),
            '1' : (os.path.join("koala_fence.png"), KoalaFence),
            '2' : (os.path.join("koala_fence_UL.png"), KoalaFence),
            '3' : (os.path.join("koala_fence_verticle.png"), KoalaFence),
            
            '4' : (os.path.join("fence.png"), DingoFence),
            '5' : (os.path.join("fence_UL.png"), DingoFence),
            '6' : (os.path.join("fence_verticle_left.png"), DingoFence),
            '7' : (os.path.join("fence_LL.png"), DingoFence),
            
            '(' : (os.path.join("reptilefence_verticle.png"), SnakeFence),
            '-' : (os.path.join("reptilefence.png"), SnakeFence),
            '&' : (os.path.join("reptilefence_UL.png"), SnakeFence),
            '*' : (os.path.join("reptilefence_UR.png"), SnakeFence),
            
            'HSF' : (os.path.join("strong_door.png"), HighStrongFence),
            
            'C' : (os.path.join("cart.png"), Car),
            'SC' : (os.path.join("cart.png"), ImperviousCar),
            '<' : (os.path.join("cart.png"), PoliceCar),
            'K' : (os.path.join("kangaroo.png"), Kangaroo),
            'T' : (os.path.join("taz.png"), Taz),
            'P' : (os.path.join("platypus.png"), Platypus),
            'A' : (os.path.join("koala.png"), Koala),
            'D' : (os.path.join("dingo.png"), Dingo),
            'BS' : (os.path.join("snake.png"), Snake),
            
            'TK' : (os.path.join("ticket_kiosk.png"), Building),
            'SK' : (os.path.join("snacks_kiosk.png"), Building),
            'DK' : (os.path.join("drink_kiosk.png"), Building),
            
            'RHR' : (os.path.join("reptilehouse_roof.png"), WalkableRoof),
            'RHF' : (os.path.join("reptilehouse_front.png"), Building),
            'RB1' : (os.path.join("reptilehouse_base_1.png"), Building),
            'RB2' : (os.path.join("reptilehouse_base_2.png"), Building),
            
            '|' : (os.path.join("tree.png"), Tree)}

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

