'''
Created on Apr 28, 2011

@author: krakauer
'''
from game_constants.client import *
from animal_info import info
from utils import image_util
from pygame import font
import game_variables

class Hud:
    
    def __init__(self, game):
        self.visitors_killed = 0
        self.zookeepers_killed = 0
        
        self.game = game
        self.screen = self.game.screen
        
        self.background = image_util.load_image("hud.png")
        
        self.name = ""
        self.portrait = image_util.load_image("blank_portrait.png")
        self.ability = ""
        self.canDrive = ""
        
        self.x = 0
        self.y = MAP_HEIGHT
        
        self.draw()
        
    def set_player(self, player):
        self.name = player.name
        (self.portrait, self.ability, self.canDrive) = info[player.name]
        self.portrait = image_util.load_image(self.portrait)
        self.draw()
    
    def add_visitor_killed(self):
        self.visitors_killed += 1
        self.draw()
    
    def add_zookeeper_killed(self):
        self.zookeepers_killed += 1
        self.draw()
    
    def draw(self):
        self.screen.blit(self.background, (self.x,self.y))
        
        self.screen.blit(self.portrait, (self.x + 11, self.y + 11))
    
        f = font.Font(font.get_default_font(), 20)
        name_text = f.render(self.name, True, (255, 255, 255))
        self.screen.blit(name_text, (self.x + 104, self.y + 30))
        
        ability_text = f.render(self.ability, True, (255, 255, 255))
        self.screen.blit(ability_text, (self.x + 286, self.y + 30))
        
        driving_text = f.render(self.canDrive, True, (255, 255, 255))
        self.screen.blit(driving_text, (self.x + 478, self.y + 30))

        visitors_text = f.render(str(self.visitors_killed), True, (255, 255, 255))
        self.screen.blit(visitors_text, (self.x + 237, self.y + 60))

        zookeeper_text = f.render(str(self.zookeepers_killed), True, (255, 255, 255))
        self.screen.blit(zookeeper_text, (self.x + 504, self.y + 60))

        x_start = 658
        y_start = 19
        x = x_start
        y = y_start
        index = 0
        for animal in game_variables.animals_freed:
            image = game_variables.animals_freed[animal]
            self.screen.blit(image, (self.x + x, self.y + y))
            x += 34
            index += 1
            if index is 3:
                y += 34
                x = x_start
            
            
