import asyncio


class Matchmaker:
    def __init__(self):
        # todo: consider using own list to provent possible buggy behavior
        self.users_queue = []

    def get_oponent(self, user_id):
        for player in self.users_queue:
            if player != user_id:
                return player
        return None

    def enter_queue(self, user_id):
        if user_id not in self.users_queue:
            self.users_queue.append(user_id)

    async def searcher(self, user_id):
        oponent = None
        while not oponent:
            oponent = self.get_oponent(user_id)
            await asyncio.sleep(0)
        self.users_queue.remove(oponent)
        return oponent


matchmaker = Matchmaker()

__all__ = ['matchmaker']
