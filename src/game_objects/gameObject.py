'''
Created on Apr 15, 2011

@author: calvin
'''
import pygame

class GameObject(pygame.sprite.Sprite):
    
    def __init__(self, image, coordinates, game):
        super(GameObject, self).__init__()
        
        self.x, self.y = coordinates
        
        self.game = game
        
        self.image = image
        
        self.rect = self.image.get_rect().move(coordinates)
        
        self.shouldRemove = False
        
    def update(self):
        raise NotImplementedError();

    def draw(self):
        raise NotImplementedError();