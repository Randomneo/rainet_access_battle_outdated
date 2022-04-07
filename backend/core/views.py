import json
from logging import getLogger

from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        log = getLogger(__name__)
        log.error('Received %s', text_data)
        user = self.scope['user']
        log.error(user)
        if not user.is_authenticated:
            self.close(code=3000)
            return

        self.send(json.dumps(text_data))
