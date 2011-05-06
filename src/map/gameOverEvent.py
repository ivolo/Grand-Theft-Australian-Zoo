from mapEvent import MapEvent
from pygame import font
import pygame
from pygame.locals import *

class GameOverEvent(MapEvent):
    
    def __init__(self, game):
        self.game = game
    
    def fire(self, source):
        screen = GameOverScreen(self.game)
        screen.draw()
        while not any(map(lambda x: x.type == KEYDOWN and x.key == K_RETURN, pygame.event.get())):
            pass
        self.game.returnToMainMenu = True
        self.game.isGameOver = True

class GameOverScreen():
    
    def __init__(self, game):
        self.game = game
        
    def draw(self):
        self.game.screen.fill((0,0,0))
        f = font.Font(font.get_default_font(), 60)
        text = f.render("YOU WIN!", True, (255,255,255))
        self.game.screen.blit(text, ((self.game.screen.get_width() - text.get_width()) / 2,
                                     (self.game.screen.get_height() - text.get_height()) / 2))
        pygame.display.flip()
    
    
        