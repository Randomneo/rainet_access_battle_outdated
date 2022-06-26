from fastapi.testclient import TestClient


def test_game(user1, auth_client: TestClient):
    with auth_client.websocket_connect('/game', headers=auth_client.headers) as wsclient:
        test_data = {
            'test': 'message',
        }
        wsclient.send_json(test_data)
        resp = wsclient.receive_json()
        assert 'type' in resp
        assert resp['type'] == 'pingback'
        assert resp['user'] == user1.username
        assert resp['data'] == test_data
