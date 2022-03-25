from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Game(models.Model):
    player1 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='game1',
    )
    player2 = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='game2',
    )

    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='wined_games',
    )
    loser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='lost_games',
    )

    created_at = models.DateTimeField(auto_now_add=True)
