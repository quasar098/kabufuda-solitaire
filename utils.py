import pygame
from os import getcwd
from os.path import join


def load_image(img_name: str):
    return pygame.image.load(join(getcwd(), "images", img_name)).convert_alpha()


def load_sound(sound_name: str):
    return pygame.mixer.Sound(join(getcwd(), "sounds", sound_name))


def mp():
    return pygame.mouse.get_pos()


def lerp_pos(p1, p2, n):
    return p1[0]*(1-n)+p2[0]*n, p1[1]*(1-n)+p2[1]*n


def clamp(n, a, b):
    return max(min(n, b), a)
