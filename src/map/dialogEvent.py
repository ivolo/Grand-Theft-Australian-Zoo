import pygame
import pygame.font as font
from pygame import Surface
from pygame.locals import *
from player.player import Player

from mapEvent import MapEvent

class DialogEvent(MapEvent):
    
    def __init__(self, text, game):
        self.text = text
        self.width = game.map_screen.get_width()
        self.height = game.map_screen.get_height() / 3
        self.game = game
        self.prev = pygame.time.get_ticks()
    
    def fire(self, source):
        
        # Sorta hacky, doesn't really reset player's move
        if pygame.time.get_ticks() - self.prev < 1500:
            return
        
        # Pause while player reads
        if isinstance(source, Player):
            dialog = self.create_dialog()
            self.game.map_screen.blit(dialog, ((self.game.map_screen.get_width() - dialog.get_width()) / 2, 
                                                             (self.game.map_screen.get_height() - dialog.get_height()) / 2))
            pygame.display.flip()
            while not any(map(lambda x: x.type == KEYDOWN and x.key == K_RETURN, pygame.event.get())):
                self.prev = pygame.time.get_ticks()
        
    def create_dialog(self):
        f = font.Font(font.get_default_font(), 30)
        text = f.render(self.text, True, (255, 255, 255))
        dialog = Surface((text.get_width() + 20, text.get_height() + 20))
        self.stroke(dialog, (255, 0, 0))
        dialog.blit(text, ((dialog.get_width() - text.get_width()) / 2, (dialog.get_height() - text.get_height()) / 2))
        return dialog
    
    def stroke(self, surface, color, width = 1):
        width = surface.get_width()
        height = surface.get_height()
        pygame.draw.line(surface, color, (0, 0), (width - 1, 0))
        pygame.draw.line(surface, color, (width - 1, 0), (width - 1, height - 1))
        pygame.draw.line(surface, color, (0, height - 1), (width - 1, height - 1))
        pygame.draw.line(surface, color, (0, 0), (0, height - 1))