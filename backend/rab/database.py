from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import configer

Base = declarative_base()


engine = create_async_engine(
    configer.get('DATABASE_URL'),
)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
