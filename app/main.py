from fastapi import FastAPI, HTTPException, status, Query
from contextlib import asynccontextmanager

from app.database import create_tables
from app.dependencies import article_depends, source_depends
from app.models.news import Article
from app.schemas.news import ArticleResponse
from app.services import ingest
from app.services import scheduler
from app.config import Settings

from sqlalchemy import Select
from datetime import datetime,timedelta,timezone

### DOING ###
# TODO : Put sources script into an API 
# TODO : /feed calling repo instead of direct 
# new TODO -> env file -> db url, db type , db file location, logs file -> PYDANTIC SETTINGS into config - doing
# new TODO -> Currently fetching from Article last 120 min -> expand options put in repo and take input from user in route return count of articles updated

################  TODO #####################
### TODO -> Error handling - doing
# new TODO -> based on db url repo subclass of Postgres, sources.py also changes 
# new TODO -> alembic migration 
# TODO :-> cleanup, db interfaces -- done
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
#print(Settings.DB_URL)




@app.get('/feed', status_code=status.HTTP_200_OK)
async def get_feed(
    article_repo : article_depends,
    minutes : int = Query(default=120,ge=30,le=10080),
    source_id : int | None = Query(default=None, ge=1),
    limit : int = Query(default=25,ge=5,le=200)
    ) -> list[ArticleResponse]:

    '''
    Dependency injection article_depends uses db_depends dependency to get database acesses and provides acesses to article repository
    ArticleRepository has method to get feed from DB
    Fetch articles from the DB.
    Validate to 

    API -> repository
    '''
    resp = await article_repo.get_feed_from_db(minutes=minutes, source_id=source_id, limit=limit)
    if not resp:
        raise HTTPException(status_code=404, detail='Not Found')
    return resp

    


@app.post('/ingest', status_code=status.HTTP_201_CREATED)
async def ingest_feed(source_repo : source_depends, article_repo : article_depends):

    # TODO : HTTP exception 
    # TODO : no new articles handle 
    # TODO : count the number of new articles ingested and LOG it in fetch and save

    '''
    Ingest articles to the DB using API instead of the scheduled job.
    API -> ingest service -> clients,repository
    '''
    await ingest.fetch_and_save_articles(source_repo, article_repo)





    


