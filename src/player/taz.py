from player import Player
from utils import image_util
from pygame import time

class Taz(Player):
    
    def __init__(self, x, y, game):
        image = image_util.load_image("taz.png")
        attack_image = image_util.load_image("taz_attack.png")
        rect = image.get_rect()
        rect.left = 5
        rect.top = 5
        rect.width = rect.width-10
        rect.height = rect.height-10
        speed = 2
        
        attack_length = 250
        
        Player.__init__(self, game, x, y, image, attack_image, rect, speed, attack_length)
   
    
