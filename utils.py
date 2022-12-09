import pygame
from os import getcwd
from os.path import join


def load_image(img_name: str):
    return pygame.image.load(join(getcwd(), "images", img_name)).convert_alpha()


def load_sound(sound_name: str):
    return pygame.mixer.Sound


def mp():
    return pygame.mouse.get_pos()
