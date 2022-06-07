from abc import ABC
from abc import abstractmethod
from logging import getLogger

from django.db.models import Q

from .ai import ai
from .board_manager import NoWinner
from .cards import Pos
from .models import Board
from .validators import SetLayoutValidator

log = getLogger(__name__)


class GameEnd(Exception):
    ...


class GameOrchestratorError(Exception):
    ...


class ActionError(GameOrchestratorError):
    ...


class Action(ABC):
    type = None
    validators = []

    def __init__(self, socket):
        self.socket = socket
        self.user = socket.scope['user']

    def load(self, data):
        for validator in self.validators:
            validator.validate(data)
        self.data = data
        return self

    @abstractmethod
    def act(self):
        ...


class SetLayoutAction(Action):
    type = 'layout'
    validators = [SetLayoutValidator()]

    def act(self):
        board = Board.load(
            player1=None,
            player2=self.user,
            board=self.data,
        )
        ai.random_layout(board)
        board.manager.exit_layout()
        board.save()

        return {
            'type': 'start game',
        }


class MoveAction(Action):
    type = 'move'

    def check_end_game(self, board):
        try:
            winner = board.manager.decide_winner()
        except NoWinner:
            return False

        self.notify_end_game(winner == self.user)
        return True

    def notify_end_game(self, is_winner):
        self.socket.send({
            'type': 'action',
            'action': {
                'type': 'endgame',
                'data': 'you' if is_winner else 'enemy'
            }
        })

    def get_board(self):
        return Board.objects\
            .filter(Q(player1=self.user) | Q(player2=self.user))\
            .order_by('-created_at')\
            .first()

    def act(self):
        board = self.get_board()
        stack = board.manager.move(
            Pos(self.data['from']['y'], self.data['from']['x']),
            Pos(self.data['to']['y'], self.data['to']['x']),
        )
        if stack:
            self.socket.send({
                'type': 'action',
                'action': {
                    'type': 'reveal',
                    'data': stack.type,
                },
            })
        if self.check_end_game(board):
            raise GameEnd()

        pos_from, pos_to = ai.make_move(board)
        stack = board.manager.move(pos_from, pos_to)

        if self.check_end_game(board):
            raise GameEnd()

        board.manager.pprint()

        return {
            'type': 'move enemy',
            'data': {
                'from': [pos_from.y, pos_from.x],
                'to': [pos_to.y, pos_to.x],
            },
        }


actions = {action.type: action for action in Action.__subclasses__()}


class GameOrchestrator:

    @staticmethod
    def process_move(socket, data):
        if 'type' not in data:
            raise GameOrchestratorError(f'No type in provided data {data}')
        if data['type'] not in actions:
            raise GameOrchestratorError('No action for provided type')

        return {
            'type': 'action',
            'action': actions[data['type']](socket).load(data['data']).act(),
        }
