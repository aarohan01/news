from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status, Query, Path

from app.routers.sources import source_router
from app.database import create_tables
from app.dependencies import article_depends, source_depends
from app.schemas.news import ArticleResponse
from app.services import ingest
from app.services import scheduler
from app.config import Settings


### DOING ###
# new TODO : Put sources script into an API -- done
# new TODO : /feed calling repo instead of direct --- done
# new TODO : -> env file -> db url, db type , db file location, logs file -> PYDANTIC SETTINGS into config - doing
# new TODO : -> Currently fetching from Article last 120 min -> 
# expand options put in repo and take input from user in route return count of articles updated - done
# new TODO : Logging of event.
# new TODO : Empty response error for feed and rss handle
# new TODO : Docstrings edit
# new TODO -> based on db url repo subclass of Postgres, sources.py also changes 


################  TODO #####################
### TODO -> Error handling - doing
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
app.include_router(source_router)



@app.get('/feed', status_code=status.HTTP_200_OK)
async def get_feed(
    article_repo : article_depends,
    minutes : Annotated[int, Query(ge=30,le=10080)] = 120,
    source_id : Annotated[int | None, Query(ge=1)] = None,
    limit : Annotated[int, Query(ge=5,le=200)] = 25
    ) -> list[ArticleResponse]:

    '''
    Dependency injection article_depends uses db_depends dependency to get database acesses and provides acesses to article repository
    ArticleRepository has method to get feed from DB
    Fetch articles from the DB.
    Validate to 

    API -> repository
    '''
    resp = await article_repo.get_feed(minutes=minutes, source_id=source_id, limit=limit)
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





    


