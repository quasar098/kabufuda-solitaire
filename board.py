import pygame
from constants import *
from utils import *
from stack import Stack
from card import Card


class Board:
    def __init__(self):
        self.y = 83
        self.board_top = load_image("backboard-top.png")
        self.board_main = load_image("backboard-main.png")
        self.stacks = [
            Stack(46, 223+83, [Card(0, 0, 3), Card(0, 0, 1), Card(0, 0, 1)]),
            Stack(174, 223+83, [Card(0, 0, 1), Card(0, 0, 5), Card(0, 0, 5)]),
            Stack(128*1+174, 233+83, [Card(0, 0, 3), Card(0, 0, 3), Card(0, 0, 3)]),
            Stack(128*2+174, 233+83, []),
            Stack(128*3+174, 233+83, []),
            Stack(128*4+174, 233+83, []),
            Stack(128*6+174, 233+83, []),
            Stack(128*5+174, 233+83, [])
        ]
        self.stacks[len(self.stacks)-1].locked = True

    @property
    def board_rect(self):
        r = self.board_top.get_rect()
        r.height += self.board_main.get_height()
        return r

    def draw(self, screen: pygame.Surface):
        screen.blit(self.board_top, (0, self.y))
        screen.blit(self.board_main, (0, self.y+202))
        for stack in self.stacks:
            stack.repos_cards()
        cards = sorted([a for b in self.stacks for a in b], key=lambda _: _.grabbed*3000+_.y)
        for card in cards:
            if not card.grabbed:
                if card.x > 300:
                    card.y -= 10
            card.draw(screen)

    def handle_event(self, event: pygame.event.Event):
        if not self.board_rect.collidepoint(mp()):
            return

        for stack in self.stacks:
            revstack = list(stack.__reversed__())
            for index, card in enumerate(revstack):

                # grab card
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if card.rect.collidepoint(mp()):

                            # check if all cards above it are same number
                            if any([check2 for check2 in revstack[:index] if check2.number != card.number]):
                                return

                            for also in revstack[:index]:
                                also.grab()

                            card.grab()
                            return

                # let go of card
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if card.grabbed:
                            card.grabbed = False

                            # check if card can go ontop of other stack
                            overlapping_stacks = [check for check in self.stacks
                                                  if check.top_rect.collidepoint(mp()) or check.top_rect.collidepoint(card.rect.center)]
                            if len(overlapping_stacks):
                                check = overlapping_stacks[0]
                                if (not len(check.cards)) or check.cards[len(check.cards)-1].number == card.number:
                                    stack.remove_cards([card])
                                    check.add_cards([card])

