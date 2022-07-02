async def test_game_no_db(auth_client):
    test_data = {
        'test': 'message',
    }
    async with auth_client.websocket_connect('/game') as wsclient:
        for i in range(10):
            await wsclient.send_json(test_data)
            resp = await wsclient.receive_json()
            assert 'type' in resp
            assert resp['type'] == 'pingback'
            assert resp['data'] == test_data
