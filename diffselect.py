import pygame
from utils import *
from constants import *
from difficulty import Difficulty
from assetloader import AssetLoader


class DifficultySelector:
    instance: "DifficultySelector" = None

    def __init__(self):
        self.has_started = False
        self.image = load_image("difficulty.png")
        self.faded = pygame.Surface((130, 80), pygame.SRCALPHA)
        self.faded.fill((255, 255, 255, 20))
        self.shown = True
        self.easy_rect = pygame.Rect(188, 148, 130, 80)
        self.medium_rect = pygame.Rect(188, 148, 130, 80).move(190, 0)
        self.hard_rect = pygame.Rect(188, 148, 130, 80).move(0, 130)
        self.expert_rect = pygame.Rect(188, 148, 130, 80).move(190, 130)
        DifficultySelector.instance = self

    def handle_event(self, event: pygame.event.Event):
        def offset(r): return r.move(self.rect.x, self.rect.y)
        if not self.shown:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if offset(self.easy_rect).collidepoint(mp()):
                    AssetLoader.play_sound(AssetLoader.select_sound)
                    self.has_started = True
                    return Difficulty.EASY
                if offset(self.medium_rect).collidepoint(mp()):
                    AssetLoader.play_sound(AssetLoader.select_sound)
                    self.has_started = True
                    return Difficulty.MEDIUM
                if offset(self.hard_rect).collidepoint(mp()):
                    AssetLoader.play_sound(AssetLoader.select_sound)
                    self.has_started = True
                    return Difficulty.HARD
                if offset(self.expert_rect).collidepoint(mp()):
                    AssetLoader.play_sound(AssetLoader.select_sound)
                    self.has_started = True
                    return Difficulty.EXPERT
                if mp()[1] > 90 and not self.rect.collidepoint(mp()) and self.has_started:
                    self.shown = False

    @property
    def rect(self):
        return self.image.get_rect(
            center=(pygame.display.get_window_size()[0] / 2, pygame.display.get_window_size()[1] / 2))

    def draw(self, screen: pygame.Surface):
        if not self.shown:
            return

        def offset(r): return r.move(self.rect.x, self.rect.y)
        screen.blit(self.image, self.image.get_rect(center=self.rect.center))
        if offset(self.easy_rect).collidepoint(mp()):
            screen.blit(self.faded, offset(self.easy_rect))
        if offset(self.medium_rect).collidepoint(mp()):
            screen.blit(self.faded, offset(self.medium_rect))
        if offset(self.hard_rect).collidepoint(mp()):
            screen.blit(self.faded, offset(self.hard_rect))
        if offset(self.expert_rect).collidepoint(mp()):
            screen.blit(self.faded, offset(self.expert_rect))

