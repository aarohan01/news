from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager

from app.database import create_tables
from app.dependencies import db_depends, article_depends, source_depends
from app.models.news import Article
from app.schemas.news import ArticleResponse
from app.services import ingest
from app.services import scheduler

from sqlalchemy import Select
from datetime import datetime,timedelta,timezone
### TODO -> Error handling - doing
# new TODO -> env file -> db url, db type , db file location, logs file 
# new TODO -> based on db url repo subclass of Postgres
# new TODO -> alembic migration 
# new TODO -> Currently fetching from Article last 120 min -> expand options put in repo and take input from user in route
# new TODO -> return count of articles updated

# TODO -> cleanup, db interfaces -- done
# TODO : Add more source -> later convert to a table -- done
# TODO : schedule injetion instead of API -- done
# TODO : Big Task Create feed -> categorise and embeddings + sematic classification + feed within a time
# TODO : Agent -> tool call, summarize 
# TODO : Auth 
# TODO : Frontend 
# TODO : frequent ingestion/frequent reads i.e. scale 
# TODO : hardcoded sources remove ? -> DB  --- done 


### DB ###
#Base.metadata.create_all(bind=engine)
@asynccontextmanager
async def lifespan(app : FastAPI):

    '''
    Context Manager for lifespan
    Do something before app starts -> yeild to app -> cleanup
    '''
    await create_tables()
    await scheduler.start_scheduler()
    yield 
    await scheduler.stop_scheduler()

### APP ###
app = FastAPI(lifespan=lifespan)


'''
@app.on_event("startup")
async def startup():
    await create_tables()
'''

@app.get('/feed', status_code=status.HTTP_200_OK)
async def get_feed(db : db_depends) -> list[ArticleResponse]:

    '''
    Dependency injection db_depends opens a session with the database
    Fetch articles from the DB 
    session runs it so ORM style
    '''
    now = datetime.now(tz=timezone.utc)
    delta = timedelta(minutes=120)
    window = now - delta
    
    stmt = Select(Article).where(Article.published >= window).order_by(Article.published.desc())
    resp = await db.scalars(stmt)

    if not resp:
        raise HTTPException(status_code=404, detail='Not Found')

    response = [ArticleResponse.model_validate(a) for a in resp.all()]
    return response
    


@app.post('/ingest', status_code=status.HTTP_201_CREATED)
async def ingest_feed(source_repo : source_depends, article_repo : article_depends):

    # TODO : HTTP exception 
    # TODO : no new articles handle 
    # TODO : count the number of new articles ingested and LOG it in fetch and save

    await ingest.fetch_and_save_articles(source_repo,article_repo)


    


    


