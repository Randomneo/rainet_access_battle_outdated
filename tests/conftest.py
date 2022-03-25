import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def auth_client(client):
    User.objects.create_user(
        username='test_auth_client',
        email='admin@example.com',
        password='password',
    )
    response = client.post('/api/token/', data={'username': 'test_auth_client', 'password': 'password'})
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.json()["access"]}')
    return client
