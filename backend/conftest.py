import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    return TestClient()


@pytest.fixture()
def user():
    return 'user1'


@pytest.fixture()
def auth_client(user, client):
    return client
