import asyncio
from abc import ABC
from abc import abstractmethod
from asyncio.mixins import _LoopBoundMixin
from logging import getLogger

from fastapi import WebSocket

from .ai import ai
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

    def __init__(self, game, player):
        self.game = game
        self.player = player

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
        board = self.game.board
        ai.random_layout(board)
        board.manager.exit_layout()
        board.save()

        return {
            'type': 'start game',
        }


class MoveAction(Action):
    type = 'move'

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

        board.manager.pprint()

        return self.game.send_to_enemy(self.player, {
            'type': 'move enemy',
            'data': self.data,
        })


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


class Player:
    def __init__(self, user, websocket: WebSocket):
        self.user = user
        self.websocket = websocket

    @property
    def is_ai(self):
        return bool(self.user)

    def __str__(self):
        return f'Player<{self.user.username}>'


class Game:
    def __init__(self, board: Board, loop):
        self.board = board
        self.await_player1 = loop.create_future()
        self.await_player2 = loop.create_future()
        self.is_end = False
        self.player1 = None
        self.player2 = None

    def make_move(self, player, move):
        move_type = move['type']
        data = move['data']
        return actions[move_type](self, player).load(data).act()

    async def turn(self, player: Player):
        move = await player.websocket.receive_json()
        return self.make_move(player, move)

    async def send(self, player, data):
        return await player.websocket.send_json(data)

    def enemy_of(self, player):
        if player == self.player1:
            return self.player2
        return self.player1

    async def send_to_enemy(self, player, data):
        enemy = self.enemy_of(player)
        if not enemy.is_ai:
            self.send(enemy, data)

    async def play(self):
        self.player1 = await self.await_player1
        log.info(f'First {str(self.player1)} entered game')
        self.player2 = await self.await_player2
        log.info(f'Second {str(self.player2)} entered game')
        while not self.is_end:
            await self.turn(self.player1)
            await self.turn(self.player2)


class MatchesOrchestrator(_LoopBoundMixin):
    games = dict()

    def get_game(self, board, loop):
        if board.id not in self.games:
            self.games[board.id] = Game(board, loop)
            self.games[board.id].play_task = asyncio.create_task(self.games[board.id].play())
        return self.games[board.id]

    def enter(self, user, board, websocket):
        # validate_board(user, board)

        game = self.get_game(board, self._get_loop())
        if board.player1 == user:
            game_player = 'await_player1'
        elif board.player2 == user:
            game_player = 'await_player2'
        else:
            assert False, 'Unknown user'
        getattr(game, game_player).set_result(Player(user, websocket))

        return game
