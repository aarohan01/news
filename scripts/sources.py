from app.database import session_local
from app.models.news import Source
from sqlalchemy import Insert
import asyncio


'''
Seed script to insert the sources.
Run manually.
'''
## TODO : DB neutral i.e. using repository
## TODO : Handle dupes i.e. given comment

sources = [{'name':'BBC', 'url':'https://feeds.bbci.co.uk/news/rss.xml', 'active': True}]

async def add_sources():

    async with session_local() as db:

        stmt = Insert(Source).values(sources)
        await db.execute(statement=stmt)
        await db.commit()


if __name__ == '__main__':
    asyncio.run(add_sources())

