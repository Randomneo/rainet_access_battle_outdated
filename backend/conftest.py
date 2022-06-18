import asyncio
from contextlib import asynccontextmanager

import pytest
from asyncpg.exceptions import InvalidCatalogNameError
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from rab.config import configer
from rab.database import Base
from rab.main import app
from rab.main import get_session
from rab.models import User


@asynccontextmanager
async def get_engine(url=None, **kwargs):
    '''
    creates engine and handle closing session for smooth db delete
    '''
    url = url or configer.get('DATABASE_TEST_URL')
    try:
        engine = create_async_engine(url, **kwargs)
        yield engine
    finally:
        await engine.dispose()


@asynccontextmanager
async def get_connection(url=None, **kwargs):
    '''
    creates engine and connects to it
    '''
    async with get_engine(url, **kwargs) as engine:
        async with engine.begin() as conn:
            yield conn


async def drop_test_db():
    '''
    delete test database
    '''
    async with get_connection(
            configer.get('DATABASE_DEFAULT_URL'),
            isolation_level='AUTOCOMMIT',
    ) as conn:
        await conn.execute(text(f'drop database {configer.get("POSTGRES_TEST_DB")}'))


async def create_test_db():
    '''
    create test db
    if already existis recreates
    '''
    try:
        async with get_connection():
            pass
    except InvalidCatalogNameError:
        pass
    else:
        await drop_test_db()

    async with get_connection(
            configer.get('DATABASE_DEFAULT_URL'),
            isolation_level='AUTOCOMMIT',
    ) as conn:
        await conn.execute(text(f'create database {configer.get("POSTGRES_TEST_DB")}'))


async def init_models():
    '''
    creates models based on metadata
    '''
    async with get_connection() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def override_get_session():
    async with get_engine() as engine:
        test_async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False,
        )

        async with test_async_session() as session:
            yield session

db_session = pytest.fixture(override_get_session)


@pytest.fixture(scope='session')
def event_loop():
    '''
    Increasing performance
    '''
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    '''
    entery point fixture

    creates test db
    initializes models
    and removes afterwards
    '''
    await create_test_db()
    await init_models()

    app.dependency_overrides[get_session] = override_get_session

    yield

    await drop_test_db()


@pytest.fixture()
def client():
    return TestClient()


@pytest.fixture()
async def user1(db_session):
    user = User(
        username='user1',
        email='user1@mail.com',
        password='password',
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture()
async def user2(db_session):
    user = User(
        username='user2',
        email='user2@mail.com',
        password='password',
    )
    db_session.add(user)
    await db_session.flush()
    return user


@pytest.fixture()
def auth_client(user, client):
    return client
