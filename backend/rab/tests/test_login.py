from ..main import app


def test_login_logout(user1, client):
    login_url = app.url_path_for('post_login')

    resp = client.post(
        login_url,
        data={
            'username': 'user',
            'password': 'password',
        },
    )
    assert resp.status_code == 200
    assert b'Username or password is incorrect' in resp.content

    resp = client.post(
        login_url,
        data={
            'username': 'user1',
            'password': 'password',
        },
    )
    assert resp.status_code == 302
    assert 'home' in resp.headers['location']

    resp = client.get(app.url_path_for('status'))
    assert resp.status_code == 200
    assert user1.username == resp.json()

    resp = client.get(app.url_path_for('logout'))
    assert resp.status_code == 200

    resp = client.get(app.url_path_for('status'))
    assert resp.status_code == 200
    assert None is resp.json()


def test_get_login_page(client):
    resp = client.get(app.url_path_for('get_login'))
    assert resp.status_code == 200
