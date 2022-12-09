import asyncio
from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from asyncpg.exceptions import InvalidCatalogNameError
from sqlalchemy import event
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette_async_wstc import TestClient

from rab.config import configer
from rab.database import Base
from rab.main import app
from rab.main import get_session
from rab.matchmaker import Matchmaker
from rab.models import User
from rab.security import hash_password


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
        await conn.execute(
            text(
                'SELECT pg_terminate_backend(pid) from pg_stat_activity where datname = '
                f"'{configer.get('POSTGRES_TEST_DB')}'"
            )
        )
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
        async with engine.connect() as conn:
            await conn.begin()

            async with sessionmaker(
                conn,
                class_=AsyncSession,
                expire_on_commit=False,
            )() as session:
                @event.listens_for(session.sync_session, 'after_transaction_end')
                def end_savepoint(session, transaction):
                    if conn.closed:
                        return
                    if not conn.in_nested_transaction():
                        conn.sync_connection.begin_nested()

                yield session
                await conn.rollback()

db_session = pytest_asyncio.fixture(override_get_session, scope='session')


@pytest.fixture(scope='session')
def event_loop():
    '''
    Increasing performance
    '''
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
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
    return TestClient(app)


@pytest.fixture(scope='session')
def default_password():
    return hash_password('password')


@pytest_asyncio.fixture()
async def user1(default_password):
    user = User(
        username='user1',
        email='user1@mail.com',
        password=default_password,
    )
    return user


@pytest_asyncio.fixture()
async def user2(default_password):
    user = User(
        username='user2',
        email='user2@mail.com',
        password=default_password,
    )
    return user


@pytest.fixture()
def auth_client_with(client):
    def get_client(user):
        resp = client.post(app.url_path_for('post_login'), {'username': user.username, 'password': 'password'})
        assert resp.status_code < 400
        return client
    return get_client


@pytest.fixture()
def auth_client(user1, auth_client_with):
    return auth_client_with(user1)


@pytest.fixture()
def matchmaker():
    return Matchmaker()
