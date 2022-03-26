def test_create_game(auth_client):
    response = auth_client.post('/api/games/')
    assert response.status_code == 201, response.content
    response = response.json()
    assert 'id' in response
    assert 'player1' in response
    assert 'created_at' in response
