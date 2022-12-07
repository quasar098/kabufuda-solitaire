import pygame
from utils import *
from constants import *


class Card:
    def __init__(self, x: int, y: int, number: int):
        self.x, self.y = x, y
        self.grabbed = False
        self.number = number
        self._gp = (0, 0)

    @property
    def image(self) -> pygame.Surface:
        return CARDS[self.number-1]

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y

    @pos.setter
    def pos(self, value) -> None:
        self.x, self.y = value

    @property
    def rect(self) -> pygame.Rect:
        return CARDS[self.number-1].get_rect(topleft=self.pos)

    def draw(self, screen: pygame.Surface):
        mp = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (0, 0, 0), self.rect.inflate(4, 4))
        screen.blit(self.image, self.rect)
        if self.grabbed:
            self.pos = mp[0]-self._gp[0], mp[1]-self._gp[1]

    def handle_event(self, event: pygame.event.Event):
        mp = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(mp):
                    self.grab()
                    return True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.grabbed = False

    def grab(self):
        mp = pygame.mouse.get_pos()
        self.grabbed = True
        self._gp = mp[0]-self.pos[0], mp[1]-self.pos[1]

    def __repr__(self):
        return f"<Card(pos={self.pos}, number={self.number}, grabbed={self.grabbed})>"
