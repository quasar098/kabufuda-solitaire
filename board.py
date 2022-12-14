import pygame
from constants import *
from utils import *
from stack import Stack
from card import Card
from random import shuffle
from assetloader import AssetLoader
from difficulty import Difficulty


class Board:
    instance: "Board" = None
    board_top = None
    board_main = None

    def quality(self):
        if self.cached_quality is None:
            q = self.depth
            q -= 2 * sum([not ((not len(stack.cards)) or stack.complete) for stack in self.top_stacks])
            q += 3 * sum([((not len(stack.cards)) or stack.complete) for stack in self.stacks])
            q += 3 * sum([stack.complete for stack in self.top_stacks])
            q += 15 * sum([stack.complete for stack in self.bottom_stacks])
            uniq = 0
            for stack in self.stacks:
                lastn = -1
                for card in stack.cards:
                    if lastn != card.number:
                        lastn = card.number
                        uniq += 1
            q -= uniq
            self.cached_quality = q
        return self.cached_quality

    def __repr__(self):
        return f"<Board(stacks={self.stacks})>"

    def __init__(self):
        self.y = 83
        self.derived = None
        self.cached_quality = None
        self.depth = 0
        if Board.board_top is None:
            Board.board_top = load_image("backboard-top.png")
        if Board.board_main is None:
            Board.board_main = load_image("backboard-main.png")
        self.top_stacks: list[Stack] = [
            Stack(302, 109, [], True, True),
            Stack(430, 109, [], True, True),
            Stack(430+128, 109, [], True, True),
            Stack(430+128+128, 109, [], True, True)
        ]
        self.bottom_stacks = [
            Stack(46, 223+83, []),
            Stack(174, 223+83, []),
            Stack(128*1+174, 223+83, []),
            Stack(128*2+174, 223+83, []),
            Stack(128*3+174, 223+83, []),
            Stack(128*4+174, 223+83, []),
            Stack(128*5+174, 223+83, []),
            Stack(128*6+174, 223+83, [])
        ]
        self.stacks = []
        self.stacks.extend(self.bottom_stacks)
        self.stacks.extend(self.top_stacks)
        Board.instance = self

    def set_difficulty(self, difficulty: Difficulty):
        for t in self.top_stacks:
            t.locked = True
        # noinspection PyTypeChecker
        for i in range(difficulty.value):
            self.top_stacks[i].locked = False

    def copy(self):
        b = Board()
        b.top_stacks = [ts.copy() for ts in self.top_stacks]
        b.bottom_stacks = [bs.copy() for bs in self.bottom_stacks]
        b.stacks = []
        b.stacks.extend(b.bottom_stacks)
        b.stacks.extend(b.top_stacks)
        b.derived = self.derived
        return b

    def randomize_game(self):
        for stack in self.stacks:
            stack.cards = []
        new_cards = []
        AssetLoader.play_sound(sound=AssetLoader.deal_sound, volume=1)
        groups = list(range(1, 11))
        anims = [_*0.426 for _ in list(range(40))]
        shuffle(anims)
        for n in groups:
            for _ in range(4):
                i = anims[0]
                new_cards.append(Card(0, 0, n, -i))
                anims.pop(0)
        shuffle(new_cards)
        for stack in self.bottom_stacks:
            for _ in range(5):
                if not len(new_cards):
                    continue
                stack.cards.append(new_cards[0])
                new_cards = new_cards[1:]

    def hash(self) -> str:
        return sha256("".join([stack.hash() for stack in self.stacks]).encode("utf-8")).hexdigest()

    def unlock_stack(self):
        for top in self.top_stacks:
            if top.locked:
                top.locked = False
                return

    def draw(self, screen: pygame.Surface):
        screen.blit(Board.board_top, (0, self.y))
        screen.blit(Board.board_main, (0, self.y+202))
        for stack in self.stacks:
            stack.draw(screen)
        cards = sorted([a for b in self.stacks for a in b], key=lambda _: _.grabbed*3000+_.y)
        for card in cards:
            card.draw(screen)
        Board.instance = self

    def handle_event(self, event: pygame.event.Event):
        def complete_set(cs_: list[Card], m=0): return len(cs_) == 4-m and list(set(map(lambda card23: card23.number, cs_))).__len__() == 1

        animing_rn = any([any([card.anim != 1 for card in stack]) for stack in self.stacks])
        if animing_rn:
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
                            AssetLoader.play_sound(AssetLoader.pickup_sound, 0.6)
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
                                    AssetLoader.play_sound(AssetLoader.place_sound, 0.6)

                                    for select in selected:
                                        select.grabbed = False

                                    # if stack was completed and is in bottom row then unlock
                                    if check.complete:
                                        if check not in self.top_stacks:
                                            self.unlock_stack()

