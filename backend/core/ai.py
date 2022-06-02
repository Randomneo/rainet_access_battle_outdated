from functools import wraps
from random import choice
from random import shuffle


class AiRetry(Exception):
    ...


def ai_retry(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        while True:
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
            *[f'{prefix}virus']*viruses,
            *[f'{prefix}link']*links,
        ]
        shuffle(cards)
        return cards

    def random_layout(self, board, invert=False):
        poses = self.start_poses
        if invert:
            poses = [[7-x, y] for x, y in poses]

        for card, pos in zip(self.random_cards(), poses):
            board.board[pos[0]][pos[1]] = card

    @ai_retry
    def make_move(self, board):
        cards = []
        for i, row in enumerate(board.board):
            for j, card in enumerate(row):
                if card.startswith('p1'):
                    cards.append({'i': i, 'j': j, 'card': card})

        card = choice(cards)
        possible_moves = [
            (card['i']-1, card['j']),
            (card['i'], card['j']-1),
            (card['i']+1, card['j']),
            (card['i'], card['j']+1),
        ]
        moves = []
        for x, y in possible_moves:
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            if board.board[x][y] not in ('virus', 'link', '_'):
                continue
            moves.append((x, y))
        try:
            move_to = choice(moves)
        except IndexError:
            raise AiRetry()
        move_from = (card['i'], card['j'])
        board.move(move_from[0], move_from[1], move_to[0], move_to[1])
        board.save()
        board.debug_board()
        board.debug_stack()
        return {
            'from': (move_from[1], move_from[0]),
            'to': (move_to[1], move_to[0]),
        }


ai = AI()
