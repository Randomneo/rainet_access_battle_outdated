import asyncio

import typer

import rab.main  # noqa
from rab.database import init_models

app = typer.Typer()


@app.command()
def create_models():
    typer.echo('creating models')
    asyncio.run(init_models())
    typer.echo('models created')


@app.command()
def create_user():
    typer.echo('user created')


if __name__ == '__main__':
    app()
