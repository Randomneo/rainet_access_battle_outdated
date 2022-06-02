import json
from abc import ABC
from abc import abstractmethod
from logging import getLogger

from django.db.models import Q

from .ai import ai
from .models import Board

log = getLogger(__name__)


class GameEnd(Exception):
    ...


class GameOrchestratorError(Exception):
    ...


class ActionError(GameOrchestratorError):
    ...


class Action(ABC):
    type = None

    def __init__(self, socket):
        self.socket = socket
        self.user = socket.scope['user']

    @staticmethod
    @abstractmethod
    def act(act_data=None):
        ...


class SetLayoutAction(Action):
    type = 'layout'

    allowed_poses = (
        (7, 0),
        (7, 1),
        (7, 2),
        (6, 3),
        (6, 4),
        (7, 5),
        (7, 6),
        (7, 7),
    )

    @staticmethod
    def validate_field(i, j, field):
        is_virus = field.startswith('virus')
        is_link = field.startswith('link')
        if (is_virus or is_link) and (i, j) not in SetLayoutAction.allowed_poses:
            raise ActionError('not valid virus/link pos')

        if is_virus:
            return 1, 0
        if is_link:
            return 0, 1
        return 0, 0

    @staticmethod
    def validate_board(board):
        viruses = 0
        links = 0
        for i, row in enumerate(board):
            for j, item in enumerate(row):
                virus, link = SetLayoutAction.validate_field(i, j, item)
                viruses += virus
                links += link
        if not (viruses == 4 and links == 4):
            raise ActionError('not valid cards count')

    def act(self, data):

        SetLayoutAction.validate_board(data)

        board = Board.objects.create(
            player2=self.user,
            board=data,
            is_player1_turn=False,
        )
        ai.random_layout(board)

        return {
            'type': 'start game',
        }


class MoveAction(Action):
    type = 'move'

    def check_end_game(self, board):
        p1_stack = board.check_stack_for_end_game(board.player1_stack)
        p2_stack = board.check_stack_for_end_game(board.player2_stack)
        p1_winner = False
        p2_winner = False
        if p1_stack == 'virus':
            p2_winner = True
        elif p1_stack == 'link':
            p1_winner = True
        elif p2_stack == 'virus':
            p1_winner = True
        elif p2_stack == 'link':
            p2_winner = True

        if p1_winner or p2_winner:
            board.set_winner(p1_winner)
            board.save()
            self.notify_end_game(p1_winner)
            return True
        return False

    def notify_end_game(self, is_winner):
        self.socket.send(json.dumps({
            'type': 'action',
            'action': {
                'type': 'endgame',
                'data': 'you' if is_winner else 'enemy'
            }
        }))

    def get_board(self):
        return Board.objects\
            .filter(Q(player1=self.user) | Q(player2=self.user))\
            .order_by('-created_at')\
            .first()

    def act(self, data):
        log.error('move action')
        log.error(data)

        # todo check move validity
        board = self.get_board()
        if board.board[data['to']['y']][data['to']['x']].startswith('p1'):
            # todo add proper way to deal with extra messages
            self.socket.send(json.dumps({
                'type': 'action',
                'action': {
                    'type': 'reveal',
                    'data': board.board[data['to']['y']][data['to']['x']][2:],
                },
            }))
        board.move(data['from']['y'], data['from']['x'], data['to']['y'], data['to']['x'])
        board.save()
        if self.check_end_game(board):
            raise GameEnd()
        response = ai.make_move(board)
        if self.check_end_game(board):
            raise GameEnd()

        return {
            'type': 'move enemy',
            'data': response,
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
            'action': actions[data['type']](socket).act(data['data']),
        }
