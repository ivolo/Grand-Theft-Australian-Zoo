import math
import pygame


def check_collision(sprite, group):
    #collision = pygame.sprite.spritecollideany(sprite, group)
    #if collision != None and collision != sprite:
    #    return True
    
    collisions = pygame.sprite.spritecollide(sprite, group, False)
    for collider in collisions:
        if collider is not sprite:
            return True
    
    return False

def get_distance(a, b):
    return  math.sqrt(((a.rect.left - b.rect.left) ** 2 + \
                       (a.rect.top - b.rect.top) ** 2))
    
