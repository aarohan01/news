'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DB_URL = "sqlite:///./db/app.db"
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={'check_same_thread':False} )
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass
'''

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DB_URL = "sqlite+aiosqlite:///./db/app.db"
async_engine = create_async_engine(SQLALCHEMY_DB_URL)
session = async_sessionmaker(autoflush=False, autocommit=False, expire_on_commit=False, bind=async_engine)


async def create_tables():
    '''
    SQLAlchemy core -> begin engine connection + action + close
    Using a context manager to avoid cleanup.
    '''
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Base(DeclarativeBase):
    pass