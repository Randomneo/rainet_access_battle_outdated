from fastapi import Depends
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from .database import async_session
from .models import *  # noqa

app = FastAPI()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@app.get('/')
async def root(session=Depends(get_session)):
    return {}
