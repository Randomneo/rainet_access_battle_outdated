from logging import getLogger

from .gameorchestrator import GameEnd
from .gameorchestrator import GameOrchestrator
from .gameorchestrator import GameOrchestratorError
from .websocket import WebsocketConsumer
from .websocket import WSClose


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def _receive(self, data):
        log = getLogger(__name__)
        log.debug('Received %s', data)
        user = self.scope['user']
        log.debug(user)

        if not user.is_authenticated:
            raise WSClose()

        try:
            self.send(GameOrchestrator.process_move(self, data))
        except GameOrchestratorError as e:
            self.send({'type': 'error', 'message': str(e)})
            log.exception(e)
        except GameEnd:
            self.send({'type': 'close'}, close=True)
