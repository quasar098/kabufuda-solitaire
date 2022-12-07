import pygame
from constants import *
from utils import *
from card import Card


class Stack:
    def __init__(self, x: int, y: int, cards: list[Card]):
        self.cards = cards
        self.x, self.y = x, y
        
    @property
    def pos(self):
        return self.x, self.y

    def handle_event(self, event: pygame.event.Event):
        for index, card in enumerate(self.cards.__reversed__()):
            if card.handle_event(event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ontop = list(self.cards.__reversed__())[:index]
                    if any(c.number != card.number for c in ontop):
                        card.grabbed = False
                    else:
                        for c in ontop:
                            c.grab()
                return card

    def top_drag_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, 90, 148) if self.cards.__len__() == 0 else self.cards[len(self.cards)-1].rect

    def draw(self, screen: pygame.Surface):
        for index, card in enumerate(self.cards):
            if not card.grabbed:
                card.pos = self.x, self.y
                card.y += index*30
            card.draw(screen)

    def __repr__(self):
        return f"<Stack(cards={self.cards})>"
