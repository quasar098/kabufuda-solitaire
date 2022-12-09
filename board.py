import pygame
from constants import *
from utils import *
from stack import Stack
from card import Card
from random import shuffle


class Board:
    instance = None

    def __init__(self):
        self.y = 83
        self.board_top = load_image("backboard-top.png")
        self.board_main = load_image("backboard-main.png")
        self.top_stacks = [
            Stack(302, 109, [], False, True),
            Stack(430, 109, [], False, True),
            Stack(430+128, 109, [], False, True),
            Stack(430+128+128, 109, [], False, True)
        ]
        self.bottom_stacks = [
            Stack(46, 223+83, []),
            Stack(174, 223+83, []),
            Stack(128*1+174, 223+83, []),
            Stack(128*2+174, 223+83, []),
            Stack(128*3+174, 223+83, []),
            Stack(128*4+174, 223+83, []),
            Stack(128*6+174, 223+83, []),
            Stack(128*5+174, 223+83, [])
        ]
        self.stacks = []
        self.stacks.extend(self.top_stacks)
        self.stacks.extend(self.bottom_stacks)
        self.randomize_game()
        self.instance = self

    def randomize_game(self):
        for stack in self.stacks:
            stack.cards = []
        new_cards = []
        groups = list(range(1, 11))
        for n in groups:
            for _ in range(4):
                new_cards.append(Card(0, 0, n))
        shuffle(new_cards)
        for stack in self.bottom_stacks:
            for _ in range(5):
                if not len(new_cards):
                    continue
                stack.cards.append(new_cards[0])
                new_cards = new_cards[1:]

    @property
    def board_rect(self):
        r = self.board_top.get_rect()
        r.height += self.board_main.get_height()
        return r

    def unlock_stack(self):
        for top in self.top_stacks:
            if top.locked:
                top.locked = False
                return

    def draw(self, screen: pygame.Surface):
        screen.blit(self.board_top, (0, self.y))
        screen.blit(self.board_main, (0, self.y+202))
        for stack in self.stacks:
            stack.draw(screen)
        cards = sorted([a for b in self.stacks for a in b], key=lambda _: _.grabbed*3000+_.y)
        for card in cards:
            card.draw(screen)

    def handle_event(self, event: pygame.event.Event):
        def complete_set(cs_: list[Card], m=0): return len(cs_) == 4-m and list(set(map(lambda card23: card23.number, cs_))).__len__() == 1

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
                                                  if check.top_rect.collidepoint(mp())]
                            if len(overlapping_stacks):
                                check = overlapping_stacks[0]

                                # stack has no cards or stack top has similar number
                                if (not len(check.cards)) or check.cards[len(check.cards)-1].number == card.number:

                                    # top row handling
                                    selected = [card for card in stack if card.grabbed]
                                    if check.show_free:  # is top row
                                        if len(check.cards):  # cards already exist there
                                            for select in selected:
                                                select.grabbed = False
                                            continue
                                        if len(selected):  # multiple cards dropped
                                            if not complete_set(selected, m=1):  # it wasn't a set of 4
                                                for select in selected:
                                                    select.grabbed = False
                                                continue
                                        if check.locked:
                                            for select in selected:
                                                select.grabbed = False
                                            continue

                                    stack.remove_cards([card])
                                    stack.remove_cards(selected)
                                    check.add_cards([card])
                                    check.add_cards(selected)
                                    for select in selected:
                                        select.grabbed = False

                                    # if stack was completed and is in bottom row then unlock
                                    if check.complete:
                                        if check not in self.top_stacks:
                                            self.unlock_stack()

