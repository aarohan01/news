from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.ingest import fetch_and_save_articles
from app.dependencies import get_source_repo, get_article_repo
from app.database import session_local

'''
Scheduler service to ingest articles
Currently no memory persistence
'''
scheduler = AsyncIOScheduler()

async def ingest_job() -> None:
    '''
    Get the dependencies of fetch_and_save_articles
    And run it.
    '''
    async with session_local() as db:
        source_repo = await get_source_repo(db)
        article_repo = await get_article_repo(db)
        await fetch_and_save_articles(source_repo, article_repo)

async def start_scheduler() -> None:
    '''
    Schedule the ingest
    '''
    scheduler.add_job(ingest_job, trigger="interval",minutes=15, id='Ingest Articles')
    scheduler.start()


async def stop_scheduler() -> None:
    '''
    Stop scheduler once app is down to cleanup.
    '''
    scheduler.shutdown()