from board import Board
from stack import Stack
from card import Card
from game import Game
from time import sleep
from typing import Optional


def available_moves(board: Board, moves_list: list[str] = None):
    if moves_list is None:
        moves_list = []
    moves: list[Board] = []
    otop: list[Stack] = board.top_stacks
    obottom: list[Stack] = board.bottom_stacks

    # bottom stack to bottom stack movement
    for x1, stack1 in enumerate(obottom):
        if not len(stack1.cards):
            continue
        tc_start = stack1.cards[-1]
        for x2, stack2 in enumerate(obottom):
            if x1 == x2:
                continue
            if len(stack2.cards):
                tc_end = stack2.cards[-1]
                if tc_end.number != tc_start.number:
                    continue
            bnew = board.copy()
            if bnew.stacks[x2].complete:
                continue
            if bnew.stacks[x1].complete:
                continue
            ncomplete = len([_ for _ in bnew.stacks if _.complete])
            ogin = bnew.stacks[x1].cards[-1].pos
            bnew.stacks[x2].cards.append(bnew.stacks[x1].cards[-1])
            bnew.stacks[x1].cards.pop()
            newcomplete = len([_ for _ in bnew.stacks if _.complete])
            if newcomplete > ncomplete:
                try_open = [os for os in bnew.stacks if os.locked]
                if len(try_open):
                    try_open[0].locked = False
            moves_list.append(f"move {x1 + 1}b to {x2 + 1}b")
            moves.append(bnew)

    # bottom stack to top stack movement (single card)
    if len([s for s in otop if not (len(s.cards) or s.locked)]):
        tindex = [index for index, ts in enumerate(board.top_stacks) if not len(ts.cards)][0]
        for bindex, bs in enumerate(obottom):
            if not len(bs.cards):
                continue
            bnew = board.copy()
            bnew.top_stacks[tindex].cards.append(bs.cards[-1])
            bnew.bottom_stacks[bindex].cards.pop()
            moves_list.append(f"move {bindex + 1}b to {tindex + 1}t")
            moves.append(bnew)

    # top stack to bottom stack movement
    for x1, tstack in enumerate(otop):
        if len(tstack.cards) != 1:
            continue
        start_tcard = tstack.cards[-1]
        for x2, nstack in enumerate(obottom):
            if len(nstack.cards):
                if nstack.cards[-1].number != start_tcard.number:
                    continue
            if nstack.complete:
                continue
            bnew = board.copy()
            ncomplete = len([_ for _ in bnew.stacks if _.complete])
            bnew.bottom_stacks[x2].cards.append(start_tcard)
            bnew.top_stacks[x1].cards.pop()
            newcomplete = len([_ for _ in bnew.stacks if _.complete])
            if newcomplete > ncomplete:
                try_open = [os for os in bnew.stacks if os.locked]
                if len(try_open):
                    try_open[0].locked = False
            moves_list.append(f"move {x1 + 1}t to {x2 + 1}b")
            moves.append(bnew)

    # bottom stack to top stack full complete
    def complete_set(cs_: list[Card], m=0):
        return len(cs_) == 4 - m and list(set(map(lambda card23: card23.number, cs_))).__len__() == 1
    for inb, bs in enumerate(board.bottom_stacks):
        if len(bs.cards) <= 4:
            continue
        if not complete_set(bs.cards[-4:]):
            continue
        for ind, ts in enumerate(board.top_stacks):
            if len(ts.cards):
                continue
            if ts.locked:
                continue
            bnew = board.copy()
            bnew.top_stacks[ind].cards.extend(bs.cards[-4:])
            bnew.bottom_stacks[inb].cards.pop()
            bnew.bottom_stacks[inb].cards.pop()
            bnew.bottom_stacks[inb].cards.pop()
            bnew.bottom_stacks[inb].cards.pop()
            moves_list.append(f"move all {inb+1}b to {ind+1}t")
            moves.append(bnew)
            break

    # bottom stack to bottom stack full movement
    for inb, bs in enumerate(board.bottom_stacks):
        if len(bs.cards) <= 4:
            continue
        if not complete_set(bs.cards[-4:]):
            continue
        for ind, ts in enumerate(board.bottom_stacks):
            if len(ts.cards):
                continue
            bnew = board.copy()
            ncomplete = len([_ for _ in bnew.stacks if _.complete])
            bnew.bottom_stacks[ind].cards.extend(bs.cards[-4:])
            bnew.bottom_stacks[inb].cards.pop()
            bnew.bottom_stacks[inb].cards.pop()
            bnew.bottom_stacks[inb].cards.pop()
            bnew.bottom_stacks[inb].cards.pop()
            newcomplete = len([_ for _ in bnew.stacks if _.complete])
            if newcomplete > ncomplete:
                try_open = [os for os in bnew.stacks if os.locked]
                if len(try_open):
                    try_open[0].locked = False
            moves_list.append(f"move all {inb+1}b to {ind+1}b")
            moves.append(bnew)
            break

    for move in moves:
        move.depth += 1
        move.derived = board.copy()
    return moves


def solve():
    hashed_so_far = []
    stack: list[Board] = [Game.board.copy()]
    for s_ in stack[0].stacks:
        for c_ in s_.cards:
            c_.anim = 1
    final: Optional[Board] = None
    print("finding solution")
    times = 0
    while len(stack):
        times += 1
        stack.sort(key=lambda b: b.quality())
        try_board: Board = stack.pop()
        if len([s for s in try_board.stacks if s.complete]) == 10:
            print("finishing recursion")
            final = try_board
            break
        for new_move in available_moves(try_board):
            if new_move.hash() not in hashed_so_far:
                hashed_so_far.append(new_move.hash())
                stack.append(new_move)

    course = []
    der = final
    while der is not None:
        course.insert(0, der)
        qwas = der.derived
        der.derived = None
        der = qwas
    Game.solution = course.copy()
    m = f"Moves: {len(course)-1}\nPositions checked: {times}\nPress spacebar for next move"
    if len(course) == 0:
        m = "There is no solution"
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements
        import win32gui
        win32gui.MessageBox(None, m, "Auto-solver", 0)
    except Exception:
        pass


def next_step():
    if Game.solution is None or not len(Game.solution):
        solve()
    if len(Game.solution) == 0:
        return
    Game.board = Game.solution[0]
    Game.solution.pop(0)


if __name__ == '__main__':
    print("no")
