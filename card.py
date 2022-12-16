import pygame
from utils import *
from constants import *
from assetloader import AssetLoader


class Card:
    ORIGIN = (430+64, -148)

    def __init__(self, x: int, y: int, number: int, anim: float = 0):
        self.x, self.y = x, y
        self.anim = anim
        self.grabbed = False
        self.number = number
        self._gp = (0, 0)

    @property
    def image(self) -> pygame.Surface:
        return AssetLoader.card_images[self.number - 1]

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y

    @pos.setter
    def pos(self, value) -> None:
        self.x, self.y = value

    @property
    def rect(self) -> pygame.Rect:
        return self.image.get_rect(topleft=self.pos)

    def draw(self, screen: pygame.Surface):
        self.anim += 4/FRAMERATE
        if self.anim > 1:
            self.anim = 1
        s_ = self.rect.inflate(4, 4)[:2]
        oawihef = lerp_pos(Card.ORIGIN, s_[:2], self.anim)
        mand = pygame.Rect(*oawihef, 94, 152)
        pygame.draw.rect(screen, (0, 0, 0), mand.inflate(2, 2))
        screen.blit(self.image, self.image.get_rect(center=mand.center))
        if self.grabbed:
            self.pos = mp()[0]-self._gp[0], mp()[1]-self._gp[1]

    def grab(self):
        self.grabbed = True
        self._gp = mp()[0]-self.pos[0], mp()[1]-self.pos[1]

    def __repr__(self):
        return f"<Card(pos={self.pos}, number={self.number}, grabbed={self.grabbed})>"
