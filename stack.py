import pygame
from constants import *
from utils import *
from card import Card
from assetloader import AssetLoader


class Stack:
    def __init__(self, x: int, y: int, cards: list[Card], lock=False, sf=False):
        self.cards = cards
        self.locked = lock
        self.show_free = sf
        self.x, self.y = x, y

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
        return pygame.Rect(self.x, self.y + 30 * max(len(self.cards)-1, 0), 90, 148)

    def draw(self, screen: pygame.Surface):
        ymod = self.complete*-1000
        for index2, card in enumerate(self.cards):
            if not card.grabbed:
                card.pos = self.x, self.y+ymod
                card.y += index2*30
        if self.show_free:
            if not self.locked:
                screen.blit(AssetLoader.free_stack_image, (self.x - 4, self.y - 4))
        if self.complete:
            screen.blit(AssetLoader.full_stack_image, (self.x - 4, self.y - 4))

    def __iter__(self):
        return iter(self.cards)

    def __repr__(self):
        return f"<Stack(cards={self.cards})>"
