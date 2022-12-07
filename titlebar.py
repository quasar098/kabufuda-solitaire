import pygame
from constants import *
from utils import *


class Titlebar:
    def __init__(self):
        self.image = load_image("controls.png")
        self.minimize_hovered = load_image("minimize-hovered.png")
        self.minimize_location = (1012, 10)
        self.close_hovered = load_image("close-hovered.png")
        self.close_location = (1044, 12)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (0, 0))
        minimize_rect = self.minimize_hovered.get_rect(topleft=self.minimize_location)
        close_rect = self.close_hovered.get_rect(topleft=self.close_location)
        if minimize_rect.collidepoint(mp()):
            screen.blit(self.minimize_hovered, self.minimize_location)
        if close_rect.collidepoint(mp()):
            screen.blit(self.close_hovered, self.close_location)

    def handle_event(self, event: pygame.event.Event):
        minimize_rect = self.minimize_hovered.get_rect(topleft=self.minimize_location)
        close_rect = self.close_hovered.get_rect(topleft=self.close_location)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if minimize_rect.collidepoint(mp()):
                    pygame.display.iconify()
                if close_rect.collidepoint(mp()):
                    pygame.quit()
                    quit()
