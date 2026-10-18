from app.repositories.base import ArticleRepository, SourceRepository
from app.schemas.news import ArticleRequest, ArticleResponse
from app.schemas.rss import SourceRead
from app.models.news import Article, Source
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import Select
from app.dependencies import AsyncSession

'''
Repo to handle Database Operations.
SQLalchemy takes care when switching DB.
Methods don't return ORM object always Pydantic schemas.
'''


class SQLArticleRepository(ArticleRepository):


    '''
    SQL DB interface implementation
    The DB to be used is decided by SQLalchemy in database.py using env file.
    Since SQLalchemy supports switching DB with minimal changes.
    '''
    
    def __init__(self, db : AsyncSession):
        
        '''
        Dependency Injection of DB session
        '''
        self.db = db


    async def save_articles_to_db(self, articles:list[ArticleRequest]) -> None:
    
        '''
        Store the articles from the rss feed to the database.
        The articles are in object so convert to dict.
        Batch insert.
        Handle dupes in DB by logging.
        No need to use a set for that batch to filter dupes
        '''


        articles_list = [a.model_dump() for a in articles]
        
        # Manual session with contextmananger is no longer required as we are using dependency injection 
        #async with session() as db:
    
        '''
        Batch insert and record dupes.
        '''
        ##### TODO : insert with failure raise error
        ## TODO : count the inserted articles and return that instead of articles
        stmt = insert(Article).values(articles_list).on_conflict_do_nothing().returning(Article)
        res = await self.db.scalars(stmt)
        res_all = res.all()
        await self.db.commit() 
    
    
        articles_reponse = [ArticleResponse.model_validate(r) for r in res_all]
        print(articles_reponse)
        #return articles_reponse


class SQLSourceRepository(SourceRepository):

    def __init__(self, db : AsyncSession):
        
        '''
        Dependency Injection of DB session
        '''
        self.db = db

    async def get_active_sources_from_db(self) -> list[SourceRead]:

        '''
        Fetch the sources from DB 
        Validate the ORM object to Pydantic Schema
        Return a list of the Source schemas
        '''

        stmt = Select(Source).where(Source.active == True)
        res = await self.db.scalars(stmt)
        res_all = res.all()   # List of Source ORM objects
        
        sources = [SourceRead.model_validate(r) for r in res_all]

        return sources
