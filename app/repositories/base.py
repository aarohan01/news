from abc import ABC, abstractmethod
from app.schemas.news import ArticleRequest, ArticleResponse 
from app.schemas.sources import SourceResponse


class ArticleRepository(ABC):

    '''
    For Article table
    '''
    @abstractmethod
    async def save_articles_to_db(self, articles:list[ArticleRequest]):
        pass 

    @abstractmethod
    async def get_feed_from_db(self, minutes : int, source_id : int | None, limit : int) -> list[ArticleResponse]:
        pass 

class SourceRepository(ABC):

    '''
    For Source table
    '''
    @abstractmethod
    async def get_active_sources_from_db(self) -> list[SourceResponse]:
        pass 