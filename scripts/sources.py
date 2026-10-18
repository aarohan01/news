from app.database import session_local
from app.models.news import Source
from sqlalchemy.dialects.sqlite import insert
import asyncio


'''
Seed script to insert the sources.
Run manually.
'''
## TODO : DB neutral i.e. using repository 
## TODO : Handle dupes i.e. given comment -- done 

sources = [
    {'name': 'BBC',          'url': 'https://feeds.bbci.co.uk/news/rss.xml',                    'active': True},
    {'name': 'NPR',          'url': 'https://feeds.npr.org/1001/rss.xml',                       'active': True},
    {'name': 'Al Jazeera',   'url': 'https://www.aljazeera.com/xml/rss/all.xml',                'active': True},
    {'name': 'The Guardian', 'url': 'https://www.theguardian.com/world/rss',                    'active': True},
    {'name': 'NYT',          'url': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'active': True},
    {'name': 'DW',           'url': 'https://rss.dw.com/rdf/rss-en-all',                        'active': False},
]

async def add_sources():

    async with session_local() as db:
        stmt = insert(Source).values(sources)
        stmt = stmt.on_conflict_do_update(
            index_elements=['url'],
            set_={'name': stmt.excluded.name, 'active': stmt.excluded.active},
        )
        await db.execute(stmt)
        await db.commit()


if __name__ == '__main__':
    asyncio.run(add_sources())

