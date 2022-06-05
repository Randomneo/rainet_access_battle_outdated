from logging import getLogger

from django.contrib.auth import get_user_model
from django.db import models

from .board_manager import BoardManager

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = BoardManager(self)

    @classmethod
    def load(cls, player1: User, player2: User, board: dict):
        return cls.objects.create(
            player1=player1,
            player2=player2,
            board=BoardManager.load(player1, player2, board),
        )

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
        self.status = self.FINISHED

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
            return 'link'
        return False
