from app.repositories.base import SourceRepository, ArticleRepository
from app.schemas.rss import RSSEntryResponse
from app.schemas.news import ArticleRequest
from app.schemas.sources import SourceResponse
from app.clients.rss import get_rss
from app.utils import time_struct_to_datetime



async def fetch_and_save_articles(source_repo: SourceRepository, article_repo : ArticleRepository):

    '''
    Input -> SourceRepository  i.e. can be either filesource or sqlsource
    Fetch Sources pass to client -> DB operation i.e. repo
    Client return the RSS entries after validating
    Convert the entries to ArticleRequest
    Save the articles -> DB operation i.e. repo
    '''
    sources_resp = await source_repo.get_active_sources_from_db()
    for s in sources_resp:
        entries = await get_rss(s)
        articles = await convert_entries_to_articles(entries, s)
        await article_repo.save_articles_to_db(articles)



           
async def convert_entries_to_articles(entries: list[RSSEntryResponse], source : SourceResponse) -> list[ArticleRequest]:
    
    ### Convert to ArticleRequest ###
    articles = []

    for entry in entries:

        article = ArticleRequest(
            title = entry.title,
            url = entry.link,
            source_id = source.id,
            summary = entry.summary,
            guid = entry.guid, 
            published = time_struct_to_datetime(entry.published_parsed)
        )

        articles.append(article)
    return articles
