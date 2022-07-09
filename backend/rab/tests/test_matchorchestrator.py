import asyncio

from ..gameorchestrator import Game
from ..gameorchestrator import MatchesOrchestrator
from ..models import Board


async def test_matchorchestrator(user1, user2, monkeypatch):
    board = Board.load(user1, user2, [[]])

    class DummyWS:
        async def send_json(self, *args, **kwargs):
            ...

        async def receive_json(self, *args, **kwargs):
            ...

    def make_move(self, *args, **kwargs):
        self.is_end = True

    monkeypatch.setattr(Game, 'make_move', make_move)

    async def enter(user):
        game = MatchesOrchestrator().enter(user, board, DummyWS())
        await game.play_task
        assert game.is_end

    task1 = asyncio.create_task(enter(user1))
    task2 = asyncio.create_task(enter(user2))

    await task1
    await task2
