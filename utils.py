import pygame
from os import getcwd
from os.path import join


def load_image(img_name: str):
    return pygame.image.load(join(getcwd(), "images", img_name)).convert_alpha()


CARDS = (
    load_image("1.png"),
    load_image("2.png"),
    load_image("3.png"),
    load_image("4.png"),
    load_image("5.png"),
    load_image("6.png"),
    load_image("7.png"),
    load_image("8.png"),
    load_image("9.png"),
    load_image("10.png")
)
BACKSIDE = load_image("backside.png")
BACKBOARD_TOP = load_image("backboard-top.png")
BACKBOARD_MAIN = load_image("backboard-main.png")
FREE_SLOT = load_image("free-slot.png")
