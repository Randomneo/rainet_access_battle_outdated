import json
from logging import getLogger

from .gameorchestrator import GameEnd
from .gameorchestrator import GameOrchestrator
from .gameorchestrator import GameOrchestratorError
from .websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def _receive(self, text_data):
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
            self.send(json.dumps(GameOrchestrator.process_move(self, data)))
        except GameOrchestratorError as e:
            self.send(json.dumps({'type': 'error', 'message': str(e)}))
            log.exception(e)
        except GameEnd:
            self.send(json.dumps({'type': 'close'}), close=True)
