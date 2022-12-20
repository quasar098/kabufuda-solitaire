import pygame
from constants import *
from utils import *
from titlebar import Titlebar
from board import Board
from assetloader import AssetLoader
from diffselect import DifficultySelector


class Game:
    board = None

    def __init__(self):
        self.win_anim = 0
        self.titlebar = Titlebar()
        if Game.board is None:
            Game.board = Board()
        self.diffselect = DifficultySelector()
        AssetLoader.init()

    def draw(self, screen: pygame.Surface):
        if AssetLoader.muted:
            AssetLoader.sound_channels[0].set_volume(0)
        else:
            AssetLoader.sound_channels[0].set_volume(1)

        Game.board.draw(screen)
        if self.diffselect.shown:
            screen.blit(AssetLoader.darken, (0, 0))
        self.titlebar.draw(screen)
        self.diffselect.draw(screen)
        if Game.has_won():
            if self.win_anim == 0:
                AssetLoader.play_sound(AssetLoader.win_sound, 0.6)
            self.win_anim += 1/FRAMERATE
        else:
            self.win_anim = 0
        if 1.3 > self.win_anim > 0:
            return
        if 1.6 > self.win_anim > 1.3:
            self.diffselect.shown = True

    def handle_event(self, event: pygame.event.Event):
        self.titlebar.handle_event(event)
        if self.diffselect.shown:
            handle = self.diffselect.handle_event(event)
            if handle is not None:
                self.diffselect.shown = False
                Game.board.set_difficulty(handle)
                Game.board.randomize_game()
            return
        Game.board.handle_event(event)

    @staticmethod
    def has_won():
        return all([stack.complete for stack in Game.board.stacks if len(stack.cards)]) \
               and any([len(stack.cards) for stack in Game.board.stacks])
