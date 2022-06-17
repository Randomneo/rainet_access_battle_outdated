from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .board_manager import BoardManager
from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Board:
    '''
    board mock migration from django
    '''

    IN_PROGRESS = 1
    FINISHED = 2
    DROPPED = 10
    STATES = (
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished'),
        (DROPPED, 'Dropped'),
    )

    def __init__(self, *args, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.player1_stack = []
        self.player2_stack = []
        self.manager = BoardManager(self)

    @classmethod
    def load(cls, player1, player2, board):
        return cls(
            player1=player1,
            player2=player2,
            board=BoardManager.load(player1, player2, board),
        )

    def set_winner(self, user):
        self.winner = self.player1 if user == self.player1 else self.player2
        self.loser = self.player2 if user == self.player1 else self.player1
        self.status = self.FINISHED
        self.save()
