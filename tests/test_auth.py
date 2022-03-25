import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


def test_login(client):
    login = 'admin'
    password = 'pass'
    User.objects.create_user(
        username=login,
        email='admin@example.com',
        password=password,
    )
    response = client.post('/api/token/', data={'username': login, 'password': password})

    assert response.status_code == 200, response.content
    response = response.json()
    assert 'access' in response
    assert 'refresh' in response
    token = response['access']

    response = client.get('/api/profile/', HTTP_AUTHORIZATION='Bearer aoe')
    assert response.status_code == 401, response.content

    response = client.get('/api/profile/', HTTP_AUTHORIZATION=f'Bearer {token}')
    assert response.status_code == 200, response.content


@pytest.mark.parametrize(
    'password,valid',
    (
        ('aoeoaeaoe', True),
        ('199873219', False),
        ('12t', False),
    ),
)
def test_password_validation(password, valid):
    if not valid:
        with pytest.raises(ValidationError):
            validate_password(password)
    else:
        validate_password(password)


def test_signup(client):
    password = 'aoeaoeaoe'
    response = client.post(
        '/api/signup/',
        data={
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': password,
        },
    )
    assert response.status_code == 201, response.content
    assert User.objects.get(email='test_user@example.com').password != password


def test_profile(auth_client):
    response = auth_client.get('/api/profile/').json()
    assert 'username' in response
    assert 'email' in response
    assert 'password' not in response
