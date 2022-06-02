from logging import getLogger

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
log = getLogger(__name__)


class Board(models.Model):
    IN_PROGRESS = 1
    FINISHED = 2
    DROPPED = 10
    STATES = (
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
        (DROPPED, 'Dropped'),
    )

    # null = AI
    player1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='boards1', null=True)
    player2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='boards2', null=True)
    state = models.CharField(max_length=32, choices=STATES, default=IN_PROGRESS)

    board = models.JSONField()
    player1_stack = models.JSONField(default=list)
    player2_stack = models.JSONField(default=list)

    is_player1_turn = models.BooleanField(default=False)
    is_player1_ai = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='won_boards', null=True)
    loser = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='lost_boards', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def stack_user(self, user_stack, item):
        user_stack.append(item)

    def stack(self, card_from, card_to):
        card = card_to
        stack = self.player1_stack
        if card.startswith('p1'):
            stack = self.player2_stack
            card = card[2:]

        if card in ('virus', 'link'):
            stack.append(card)
        if card == 'exit':
            stack.append(card_from[2:] if card_from.startswith('p1') else card_from)
        self.save()

    def set_winner(self, is_p1):
        self.winner = self.player1 if is_p1 else self.player2
        self.loser = self.player2 if is_p1 else self.player1

    def check_stack_for_end_game(self, stack):
        viruses = 0
        links = 0
        for card in stack:
            if card == 'virus':
                viruses += 1
            if card == 'link':
                links += 1
        if viruses > 3:
            return 'virus'
        if links > 3:
            return 'links'
        return False

    def move(self, x1, y1, x2, y2):
        # 1 - from, 2 - to
        self.stack(self.board[x1][y1], self.board[x2][y2])
        self.board[x2][y2] = self.board[x1][y1]
        self.board[x1][y1] = '_'

    def item_to_char(self, item):
        if item.startswith('p1'):
            return f'1{item[2:][0]}'
        if item in ('virus', 'link'):
            return f'2{item[0]}'
        return f' {item[0]}'

    def debug_stack(self):
        log.error('user1 stack:')
        for card in self.player1_stack:
            log.error(card)

        log.error('user2 stack:')
        for card in self.player2_stack:
            log.error(card)

    def debug_board(self):
        log.error('board')
        for row in self.board:
            frow = ''
            for item in row:
                frow += f' {self.item_to_char(item)}'
            log.error(frow)
