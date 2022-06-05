import json

from channels.generic.websocket import WebsocketConsumer as ChannelsWSC


class WSSend(Exception):
    def __init__(self, data=None, *args, **kwargs):
        self.data = data or {}


class WSClose(WSSend):
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
        try:
            self._receive(text_data=text_data, bytes_data=bytes_data)
        except WSClose as e:
            self.close(code=e.code)
        except WSSend as e:
            self.send(json.dumps(e.data))
