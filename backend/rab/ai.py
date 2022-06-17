from functools import wraps
from random import choice
from random import shuffle

from .cards import Pos
from .cards import load_card


class AiRetry(Exception):
    ...


def ai_retry(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        for i in range(20):
            try:
                return func(*args, **kwargs)
            except AiRetry:
                pass
    return decorator


class AI:
    start_poses = [
        [0, 0],
        [0, 1],
        [0, 2],
        [1, 3],
        [1, 4],
        [0, 5],
        [0, 6],
        [0, 7],
    ]

    def random_cards(self, viruses=4, links=4, prefix='p1'):
        cards = [
            *['virus']*viruses,
            *['link']*links,
        ]
        shuffle(cards)
        return cards

    def random_layout(self, board, player=None, invert=False):
        poses = self.start_poses
        if invert:
            poses = [[7-x, y] for x, y in poses]

        for card, pos in zip(self.random_cards(), poses):
            board.manager.add(load_card({
                'type': card,
                'owner': player,
                'x': pos[0],
                'y': pos[1],
            }))

    @ai_retry
    def make_move(self, board):
        card = choice(board.manager.user_cards(None))
        possible_moves = [
            Pos(card.pos.x - 1, card.pos.y),
            Pos(card.pos.x, card.pos.y - 1),
            Pos(card.pos.x + 1, card.pos.y),
            Pos(card.pos.x, card.pos.y + 1),
        ]
        moves = []
        for pos in possible_moves:
            if board.manager.user_can_move_here(None, pos):
                moves.append(pos)
        try:
            move_to = choice(moves)
        except IndexError:
            raise AiRetry()
        return card.pos, move_to


ai = AI()
