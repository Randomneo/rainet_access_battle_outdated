from asyncio.mixins import _LoopBoundMixin
from collections import deque


class MMQueue(_LoopBoundMixin):
    # todo: Add waiters autorestarer task

    def __init__(self):
        super().__init__()
        self.queue = []
        self.waiters = deque()

    def pop_not_waiter(self):
        while self.waiters:
            waiter = self.waiters.popleft()
            if not waiter.done():
                waiter.set_result(None)
                break

    def enter_queue(self, user_id):
        if user_id not in self.queue:
            self.queue.append(user_id)
            self.pop_not_waiter()

    def get_oponent(self, user_id):
        for player in self.queue:
            if player != user_id:
                return player
        return None

    async def search_oponent(self, user_id):
        self.enter_queue(user_id)
        oponent = self.get_oponent(user_id)
        while not oponent:
            waiter = self._get_loop().create_future()
            self.waiters.append(waiter)
            await waiter
            oponent = self.get_oponent(user_id)
        self.queue.remove(oponent)
        return oponent


class Matchmaker:
    def __init__(self):
        # todo: consider using own list to provent possible buggy behavior
        self.mmqueue = MMQueue()
        self.player_boards = {}

    async def search_oponent(self, user_id):
        return await self.mmqueue.search_oponent(user_id)

    async def build_board(self, player1, player2, board_builder):
        if (player2, player1) in self.player_boards:
            board = self.player_boards[(player2, player1)]
            del self.player_boards[(player2, player1)]
            return board

        self.player_boards[(player1, player2)] = await board_builder(player1, player2)
        return self.player_boards[(player1, player2)]


matchmaker = Matchmaker()

__all__ = ['matchmaker']
