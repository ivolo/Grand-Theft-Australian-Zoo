import pygame

def check_collision(sprite, group):
    collision = pygame.sprite.spritecollideany(sprite, group)
    if collision != None and collision != sprite:
        return True
    return False