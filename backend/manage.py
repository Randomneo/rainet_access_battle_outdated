import asyncio

import typer

import rab.main  # noqa
from rab.database import async_session
from rab.models import User

app = typer.Typer()


@app.command()
def create_user(
        username: str,
        email: str = None,
        password: str = typer.Option(..., prompt=True, hide_input=True)

):
    email = email or f'{username}@mail.com'
    user = User.create(
        username=username,
        email=email,
        password=password,
    )

    async def save_user(user):
        async with async_session() as session:
            session.add(user)
            await session.commit()

    asyncio.run(save_user(user))
    typer.echo(f'user (username={username}) created')


if __name__ == '__main__':
    app()
