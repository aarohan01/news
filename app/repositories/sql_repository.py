from app.repositories.base import ArticleRepository, SourceRepository
from app.schemas.news import ArticleRequest, ArticleResponse
from app.schemas.sources import SourceRequest, SourceResponse, SourceUpdate
from app.models.news import Article, Source

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta, timezone

'''
Repo to handle Database Operations.
SQLalchemy takes care when switching DB.
IMPORTANT : Methods don't return ORM object always Pydantic schemas.Validate here.
'''
# TODO : error handling

class SQLSourceRepository(SourceRepository):

    def __init__(self, db : AsyncSession):
        
        '''
        Dependency Injection of DB session
        '''
        self.db = db

    """
    async def get_active_sources_from_db(self) -> list[SourceResponse]:

        '''
        Fetch the sources from DB 
        Validate the ORM object to Pydantic Schema
        Return a list of the Source schemas
        '''

        stmt = select(Source).where(Source.active == True)
        res = await self.db.scalars(stmt)
        res_all = res.all()   # List of Source ORM objects
        
        sources = [SourceResponse.model_validate(r, from_attributes=True) for r in res_all]

        return sources

    """

    async def get_sources(self, active : bool | None = None) -> list[SourceResponse] | None:

        '''
        Fetch the sources from DB 
        Validate the ORM object to Pydantic Schema
        Return a list of the Source schemas
        '''

        stmt = select(Source)
        if active is not None:
            stmt = stmt.where(Source.active == active)
        res = await self.db.scalars(stmt)
        res_all = res.all()   # List of Source ORM objects
        
        sources = [SourceResponse.model_validate(r, from_attributes=True) for r in res_all]

        return sources
    
    async def get_source(self, source_id: int) -> SourceResponse | None:

        '''
        Get source to DB
        '''
        # TODO : error
        stmt = select(Source).where(Source.id == source_id)
        resp = await self.db.scalar(stmt)         # Scalar preferred in select
        if resp :
            source = SourceResponse.model_validate(resp, from_attributes=True)
        else:
            source = None

        return source

    async def add_source(self, source : SourceRequest) -> None:

        '''
        Add source to DB
        '''
        # TODO : error
        stmt = insert(Source).values(source.model_dump())
        await self.db.execute(stmt)
        await self.db.commit()


    async def update_source(self, source_id: int, source: SourceUpdate) -> None:
        '''
        Update source in DB
        '''
        # TODO : errors
        # TODO : empty dict and null name
        stmt = update(Source).where(Source.id == source_id).values(source.model_dump(exclude_unset=True))
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete_source(self, source_id: int) -> None:

        '''
        Delete source from DB
        '''
        # TODO : error not found
        stmt = delete(Source).where(Source.id == source_id)
        await self.db.execute(stmt)
        await self.db.commit()

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
        ##### TODO : insert LOG the amount of articles inserted from which sources, and report dupes
        ## TODO : No new articles based on that, which is not an error  
        if articles_list:
            stmt = insert(Article).values(articles_list).on_conflict_do_nothing(index_elements=['url']).returning(Article)
            res = await self.db.scalars(stmt)
            res_all = res.all()
            await self.db.commit() 
    
    
            articles_reponse = [ArticleResponse.model_validate(r, from_attributes=True) for r in res_all]
            #print([r.model_dump() for r in articles_reponse])
            #return articles_reponse

    async def get_feed_from_db(self, minutes : int, source_id : int | None, limit : int ) -> list[ArticleResponse]:


        # Time 
        now = datetime.now(tz=timezone.utc)
        delta = timedelta(minutes=minutes)
        window = now - delta
        stmt = select(Article).where(Article.published >= window).order_by(Article.published.desc())
        
        # Source
        if source_id:
            stmt = stmt.where(Article.source_id == source_id)

        # Limit
        stmt = stmt.limit(limit=limit)

    
        resp = await self.db.scalars(stmt)
        feed = [ArticleResponse.model_validate(a) for a in resp.all()]

        return feed

    

