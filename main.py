from fastapi import FastAPI, HTTPException, status
from clients import rss
from database import create_tables
from contextlib import asynccontextmanager
from dependencies import db_depends
from sqlalchemy import Select
from models.news import Article
from schemas.news import ArticleResponse

### TODO -> Error handling, cleanup, db interfaces 
# TODO : Add more source -> later convert to a table 
# TODO : schedule injetion instead of API 
# TODO : Big Task Create feed -> categorise and embeddings + sematic classification + feed within a time
# TODO : Agent -> tool call, summarize 
# TODO : SQLite to PostGres/MySQL
# TODO : Auth 
# TODO : Frontend 
# TODO : frequent ingestion/frequent reads i.e. scale 
# TODO : hardcoded sources remove ? -> DB


### DB ###
#Base.metadata.create_all(bind=engine)
@asynccontextmanager
async def lifespan(app : FastAPI):

    '''
    Context Manager for lifespan
    Do something before app starts -> yeild to app -> cleanup
    '''
    await create_tables()
    yield 
    

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
    # TODO : Currently fetching from Article -> need to fetch from a created feed5

    stmt = Select(Article)
    resp = await db.scalars(stmt)

    if not resp:
        raise HTTPException(status_code=404, detail='Not Found')

    response = [ArticleResponse.model_validate(a) for a in resp.all()]
    return response
    


@app.post('/ingest', status_code=status.HTTP_201_CREATED)
async def ingest_feed():

    # TODO : HTTP exception 
    # TODO : no new articles handle 
    resp = await rss.fetch_and_store_articles()
    if not resp:
        raise HTTPException(status_code=404)
    return resp

    


    


