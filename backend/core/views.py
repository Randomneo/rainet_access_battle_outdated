import json
from logging import getLogger

from channels.generic.websocket import WebsocketConsumer

from .gameorchestrator import GameOrchestrator
from .gameorchestrator import GameOrchestratorError


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        log = getLogger(__name__)
        log.debug('Received %s', text_data)
        user = self.scope['user']
        log.debug(user)

        if not user.is_authenticated:
            self.close(code=3000)
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            raise

        try:
            self.send(json.dumps(GameOrchestrator.process_move(data)))
        except GameOrchestratorError as e:
            self.send(json.dumps({'type': 'error', 'message': str(e)}))
            log.exception(e)
