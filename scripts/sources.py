from app.database import session_local
from app.models.news import Source
from sqlalchemy.dialects.sqlite import insert
import asyncio


'''
Seed script to insert the sources.
Run manually.
'''
## TODO : DB neutral i.e. using repository
## TODO : Handle dupes i.e. given comment

sources = [
    {'name': 'BBC', 'url': 'https://feeds.bbci.co.uk/news/rss.xml', 'active': True},
    {'name': 'NPR', 'url': 'https://feeds.npr.org/1001/rss.xml', 'active': True},
]

async def add_sources():

    async with session_local() as db:

        stmt = insert(Source).values(sources).on_conflict_do_nothing(index_elements=['url'])
        await db.execute(statement=stmt)
        await db.commit()


if __name__ == '__main__':
    asyncio.run(add_sources())

