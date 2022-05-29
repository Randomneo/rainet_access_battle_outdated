from logging import getLogger
from random import choice
from random import shuffle

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
log = getLogger(__name__)


class Board(models.Model):
    # null = AI
    player1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='boards1', null=True)
    player2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='boards2', null=False)

    board = models.JSONField()
    player1_stack = models.JSONField(default=list)
    player2_stack = models.JSONField(default=list)

    is_player1_turn = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # AI func
    def ai_set_layout(self):
        cards = [*['p1virus']*4, *['p1link']*4]
        shuffle(cards)
        poses = [
            [0, 0],
            [0, 1],
            [0, 2],
            [1, 3],
            [1, 4],
            [0, 5],
            [0, 6],
            [0, 7],
        ]
        for i, pos in enumerate(poses):
            x, y = pos
            self.board[x][y] = cards[i]

    def ai_make_move(self):
        cards = []
        for i, row in enumerate(self.board):
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
            if self.board[x][y] not in ('virus', 'link', '_'):
                continue
            moves.append((x, y))
        # todo: handle no moves error
        move_to = choice(moves)
        move_from = (card['i'], card['j'])
        stack = self.move(move_from[0], move_from[1], move_to[0], move_to[1])
        self.save()
        self.debug_board()
        return {
            'from': (move_from[1], move_from[0]),
            'to': (move_to[1], move_to[0]),
            'stack': stack,
        }

    def move(self, x1, y1, x2, y2):
        # 1 - from, 2 - to
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = '_'

    def item_to_char(self, item):
        if item.startswith('p1'):
            return f'1{item[2:][0]}'
        return f'2{item[0]}'

    def debug_board(self):
        log.error('board')
        for row in self.board:
            frow = ''
            for item in row:
                frow += f' {self.item_to_char(item)}'
            log.error(frow)
