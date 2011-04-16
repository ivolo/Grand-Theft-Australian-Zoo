import os, sys
import pygame
import math

from pygame.locals import *

# Shamelessly stolen from http://www.pygame.org/wiki/RotateCenter
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def get_angle(source, dest):
    s_x = source[0]
    s_y = source[1]

    d_x = dest[0]
    d_y = dest[1]

    x_diff = d_x - s_x
    y_diff = d_y - s_y

    angle = math.pi/2.0
    if float(y_diff) != 0:
        angle = math.atan(x_diff/float(y_diff))

    extra_rotation = 0
    if y_diff < 0:
        extra_rotation = 180
    elif y_diff is 0:
        if x_diff < 0:
            extra_rotation = 180

    return angle*180/math.pi - extra_rotation

# Stolen shamelessly from http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/
def load_sliced_sprites(self, w, h, filename):
    '''
    Specs :
        Master can be any height.
        Sprites frames width must be the same width
        Master width must be len(frames)*frame.width
    Assuming you ressources directory is named "ressources"
    '''
    images = []
    master_image = pygame.image.load(os.path.join('images', filename)).convert_alpha()
 
    master_width, master_height = master_image.get_size()
    for j in xrange(int(master_height/h)):
        for i in xrange(int(master_width/w)):
            images.append(master_image.subsurface((i*w,j*h,w,h)))
    return images

def load_image(filename):
    image = pygame.image.load(os.path.join('images',filename)).convert_alpha()
    return image