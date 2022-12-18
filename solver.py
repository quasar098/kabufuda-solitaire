from board import Board
from stack import Stack
from card import Card
from game import Game


def available_moves(board: Board, moves_list: list[str]):
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
            bnew.stacks[x2].cards.append(bnew.stacks[x1].cards[-1])
            bnew.stacks[x1].cards.pop()
            if bnew.stacks[x2].complete:
                try_open = [os for os in bnew.stacks if os.locked]
                if len(try_open):
                    try_open[0].locked = False
            moves_list.append(f"move {x1+1}b to {x2+1}b")
            moves.append(bnew)

    # bottom stack to top stack movement
    if len([s for s in otop if not (len(s.cards) or s.locked)]):
        tindex = [index for index, ts in enumerate(board.top_stacks) if not len(ts.cards)][0]
        for bindex, bs in enumerate(obottom):
            if not len(bs.cards):
                continue
            bnew = board.copy()
            bnew.top_stacks[tindex].cards.append(bs.cards[-1])
            bnew.bottom_stacks[bindex].cards.pop()
            moves_list.append(f"move {bindex+1}b to {tindex+1}t")
            moves.append(bnew)

    # top stack to bottom stack movement
    for x1, tstack in enumerate(otop):
        if not len(tstack.cards):
            continue
        start_tcard = tstack.cards[-1]
        for x2, nstack in enumerate(obottom):
            if len(nstack.cards):
                if nstack.cards[-1].number != start_tcard.number:
                    continue
            if nstack.complete:
                continue
            bnew = board.copy()
            bnew.bottom_stacks[x2].cards.append(start_tcard)
            bnew.top_stacks[x1].cards.pop()
            if bnew.bottom_stacks[x2].complete:
                try_open = [os for os in bnew.stacks if os.locked]
                if len(try_open):
                    try_open[0].locked = False
            moves_list.append(f"move {x1+1}t to {x2+1}b")
            moves.append(bnew)

    return moves


def solve():
    hashed_so_far = []
    possible_one = []

    def recurs(b, ml=None):
        if ml is None:
            ml = []
        amoves = available_moves(b, ml)
        for move in amoves:
            if move.hash() not in hashed_so_far:
                hashed_so_far.append(move.hash())
                if len([_ for _ in move.stacks if _.complete]) == 2:
                    possible_one.append(move)


                    return True
                if recurs(move, list(tuple(ml))):
                    return True

    recurs(Board.instance)


if __name__ == '__main__':
    solve()
