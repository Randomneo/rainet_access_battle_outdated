from pyconfiger import configer
from pyconfiger import key_builder


def database_url_builder(user, password, db_host, port, db_name):
    return f'postgresql://{user}:{password}@{db_host}:{port}/{db_name}'


@key_builder(use=(
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'DB_HOST',
    'POSTGRES_PORT',
    'POSTGRES_DB',
))
def database_url(*args):
    return database_url_builder(*args)


@key_builder(use=(
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'DB_HOST',
    'POSTGRES_PORT',
    'POSTGRES_TEST_DB',
))
def test_database_url(*args):
    return database_url_builder(*args)


configer.required_keys = (
    'POSTGRES_DB',
    'POSTGRES_TEST_DB',
    'POSTGRES_USER',
    'POSTGRES_PASSWORD',
    'POSTGRES_PORT',
    'DB_HOST',
)
configer.built_keys['DATABASE_URL'] = database_url
configer.built_keys['TEST_DATABASE_URL'] = test_database_url


DATABASE_URL = configer.get('DATABASE_URL')
