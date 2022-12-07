import pygame
from constants import *
from utils import *


class ImageLoader:
    card_images = []

    @staticmethod
    def init():
        ImageLoader.card_images = [
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
        ]
