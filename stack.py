import pygame
from constants import *
from utils import *
from card import Card


class Stack:
    def __init__(self, x: int, y: int, cards: list[Card]):
        self.cards = cards
        self.free_image = None
        self.complete_image = None
        self.locked = False
        self.x, self.y = x, y

    def init_images(self):
        if not self.free_image:
            self.free_image = load_image("free-slot.png")

    @property
    def complete(self):
        return len(self.cards) == 4 and list(set(map(lambda card: card.number, self.cards))).__len__() == 1

    @property
    def pos(self):
        return self.x, self.y

    def add_cards(self, cards: list[Card]):
        self.cards.extend(cards)

    def remove_cards(self, cards: list[Card]):
        self.cards = [card for card in self.cards if card not in cards]

    def __reversed__(self):
        return self.cards.__reversed__()

    @property
    def top_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, 90, 148 + 30 * len(self.cards))

    def repos_cards(self):
        for index, card in enumerate(self.cards):
            if not card.grabbed:
                card.pos = self.x, self.y
                card.y += index*30

    def __iter__(self):
        return iter(self.cards)

    def __repr__(self):
        return f"<Stack(cards={self.cards})>"
