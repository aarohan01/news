'''
from typing import Annotated
from database import session
from sqlalchemy.orm import Session
from fastapi import Depends


def get_db():

    with session() as db:
        yield db


db_depends = Annotated[Session,Depends(get_db)]
'''

from typing import Annotated
from app.database import session_local
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_db():

    async with session_local() as db:
        yield db


db_depends = Annotated[AsyncSession,Depends(get_db)]