import feedparser
from httpx import AsyncHTTPTransport, HTTPTransport, HTTPError, Client, AsyncClient

from app.utils import pretty_print, run_async, time_struct_to_datetime
from app.schemas.rss import ParseResponse
from app.schemas.news import ArticleRequest, ArticleResponse
from app.dependencies import AsyncSession
from app.repositories.

from pydantic import ValidationError


'''
Connect to sources, get the RSS files, validate, convert to appropriate models/schemas and pass on to ingest service
'''



## SOURCES ##
#sources = {'BBC': 'https://feeds.bbci.co.uk/news/rss.xml'
#           }


## Clients ##
async_client = AsyncClient(timeout=10.0, transport=AsyncHTTPTransport(retries=3))
#client = Client(timeout=10.0, transport=HTTPTransport(retries=3))



### ###
async def test(db : AsyncSession):




async def fetch_and_store_articles(db : AsyncSession) -> list[ArticleResponse]:

    '''
    Get RSS feed of the source.
    Convert to entries and validate at boundary.
    Convert to articles to normalize
    Convert to ORM object and store in db
    '''
    articles_responses = []
    for source in sources.keys():
        
        entries = await get_rss(source)
        articles = await convert_entries_to_articles(entries, source)
        articles_responses.append(await save_articles(articles))

    return articles_responses

async def get_rss(source: str) -> list[ParseResponse] :

    try:
        response = await async_client.get(sources[source])
        response.raise_for_status() 
    except HTTPError:
        print(f'Error fetching {source} articles...')
        return []


    parsed_response = feedparser.parse(response.content)
    if parsed_response.bozo == 1:
        print(f'Error parsing {source} articles')
        return []
    
    #print(len(parsed_response['entries']))
    parsed_entries = parsed_response.entries

    
    #pretty_print(parsed_entries[0])
    #print(type(parsed_entries[0]['published_parsed']))

    ### Validation ###
    validated_entries = []
    for entry in parsed_entries:

        try:
            validated_entry = ParseResponse.model_validate(entry)
        except ValidationError:
            print("Failed entry parsing validation...")
        else:
            validated_entries.append(validated_entry)


    return validated_entries

            
async def convert_entries_to_articles(entries: list[ParseResponse], source: str) -> list[ArticleRequest]:
    
    ### Convert to ArticleRequest ###
    articles = []

    for entry in entries:

        article = ArticleRequest(
            title = entry.title,
            url = entry.link,
            source = source,
            summary = entry.summary,
            guid = entry.guid, 
            published = time_struct_to_datetime(entry.published_parsed)
        )

        articles.append(article)
    return articles



"""
async def save_articles(articles:list[ArticleRequest]) -> list[ArticleResponse]:


    # articles -> might contain dupes 
    # db table articles ->  might contain dupes
    # to avoid article dupes can put in a set to check
    # to avoid db dupes use upsert


    '''
    ### Let DB handle conflict and throw an error ###
    url_set = set()
    articles_dict = []
    for a in articles:
        if a.url not in url_set:
            url_set.add(a.url)
            articles_dict.append(a.model_dump())
    '''
    
    
    articles_list = [a.model_dump() for a in articles]
    async with session() as db:

        # No need as we are using insert(Core) not add(ORM style)
        # db_article = Article(**article.model_dump())
        

        # Dupes give unique key error can't be handled by add (ORM way)
        # db.add(db_article)
        # stmt = Insert(table='articles').on_conflict_do_nothing.values(**db_article.model_dump())

        ##### TODO : insert with failure raise error
        stmt = insert(Article).values(articles_list).on_conflict_do_nothing(index_elements=['url']).returning(Article)
        res = await db.scalars(stmt)
        res_all = res.all()
        await db.commit() 


    articles_reponse = [ArticleResponse.model_validate(r) for r in res_all]
    #print(articles_reponse)
    return articles_reponse
"""
                

    


if __name__ == "__main__":

    run_async(get_rss, 'BBC')





