import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def user():
    return User.objects.create_user(
        username='test_auth_client',
        email='admin@example.com',
        password='password',
    )


@pytest.fixture()
def auth_client(user, client):
    client.login(username=user.username, password='password')
    return client
