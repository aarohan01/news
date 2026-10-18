import feedparser
from httpx import AsyncHTTPTransport, HTTPTransport, HTTPError, Client, AsyncClient

from app.utils import pretty_print
from app.schemas.sources import SourceResponse
from app.schemas.rss import RSSEntryResponse

from pydantic import ValidationError



## Clients ##
async_client = AsyncClient(timeout=10.0, transport=AsyncHTTPTransport(retries=3))
#client = Client(timeout=10.0, transport=HTTPTransport(retries=3))



async def get_rss(source: SourceResponse) -> list[RSSEntryResponse] :

    try:
        response = await async_client.get(source.url)
        response.raise_for_status() 
    except HTTPError:
        print(f'Error fetching {source.name} articles...')
        return []


    parsed_response = feedparser.parse(response.content)
    if parsed_response.bozo == 1:
        print(f'Error parsing {source} articles')
        return []
    

    parsed_entries = parsed_response.entries
    
    #pretty_print(parsed_entries[0])

    ### Validation ###
    validated_entries = []
    for entry in parsed_entries:

        try:
            validated_entry = RSSEntryResponse.model_validate(entry)
        except ValidationError as e:
            print(f"Failed entry parsing validation for source {source.id}...{e}")
        else:
            validated_entries.append(validated_entry)


    return validated_entries








