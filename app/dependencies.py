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
from app.repositories.base import SourceRepository, ArticleRepository
from app.repositories.sql_repository import SQLSourceRepository, SQLArticleRepository

async def get_db():

    async with session_local() as db:
        yield db

db_depends = Annotated[AsyncSession, Depends(get_db)]


# TODO : Add a switch for filerepo
async def get_source_repo(db : db_depends) -> SourceRepository:
    return SQLSourceRepository(db)

async def get_article_repo(db : db_depends)-> ArticleRepository:
    return SQLArticleRepository(db)


# Type of Interface and implemented using the sql implemtation.
source_depends = Annotated[SourceRepository, Depends(get_source_repo)]
article_depends = Annotated[ArticleRepository, Depends(get_article_repo)]