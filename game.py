import pygame
from constants import *
from utils import *
from titlebar import Titlebar
from board import Board
from imageloader import ImageLoader


class Game:
    def __init__(self):
        self.titlebar = Titlebar()
        self.board = Board()
        ImageLoader.init()

    def draw(self, screen: pygame.Surface):
        self.board.draw(screen)
        self.titlebar.draw(screen)

    def handle_event(self, event: pygame.event.Event):
        self.board.handle_event(event)
        self.titlebar.handle_event(event)
