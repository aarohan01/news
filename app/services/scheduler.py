from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.ingest import fetch_and_save_articles


'''
Scheduler service to ingest articles
Currently no memory persistence
'''

async def schedule_ingest() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_and_save_articles,args=[], trigger="interval",minutes=15, id='Ingest Articles')
    scheduler.start()
