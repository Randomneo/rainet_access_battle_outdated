import enum

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from .board_manager import BoardManager
from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Board(Base):
    __tablename__ = 'board'

    class Statuses(enum.Enum):
        in_progress = 1
        finished = 2
        dropped = 10

    id = Column(Integer, primary_key=True)

    player1_id = Column(Integer, ForeignKey(User.id, onupdate='CASCADE', ondelete='SET NULL'))
    player2_id = Column(Integer, ForeignKey(User.id, onupdate='CASCADE', ondelete='SET NULL'))
    winner_id = Column(Integer, ForeignKey(User.id, onupdate='CASCADE', ondelete='SET NULL'))
    loser_id = Column(Integer, ForeignKey(User.id, onupdate='CASCADE', ondelete='SET NULL'))

    board = Column(JSON)
    player1_stack = Column(JSON, default=list, server_default='[]', nullable=False)
    player2_stack = Column(JSON, default=list, server_default='[]', nullable=False)
    status = Column(
        Enum(Statuses),
        default=Statuses.in_progress,
        server_default=str(Statuses.in_progress.name),
        nullable=False,
    )

    player1 = relationship(User)
    player2 = relationship(User)
    winner = relationship(User)
    loser = relationship(User)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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