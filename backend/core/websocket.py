import json

from channels.generic.websocket import WebsocketConsumer as ChannelsWSC


class WSClose(Exception):
    def __init__(self, code=3000, *args, **kwargs):
        self.code = code
        super().__init__(*args, **kwargs)


class WebsocketConsumer(ChannelsWSC):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def _receive(self, text_data=None, bytes_data=None):
        pass

    def receive(self, text_data=None, bytes_data=None):
        assert not bytes_data, '`bytes_data` is not allowed in this implementation'
        try:
            self._receive(data=json.loads(text_data))
        except WSClose as e:
            self.close(code=e.code)
        except json.JSONDecodeError as e:
            self.send({
                'type': 'error',
                'message': str(e),
            })

    def send(self, data, *args, **kwargs):
        super().send(text_data=json.dumps(data), *args, **kwargs)
