from abc import ABC, abstractmethod
from app.schemas.news import ArticleRequest, ArticleResponse 
from app.schemas.sources import SourceRequest, SourceResponse, SourceUpdate


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
    async def add_source(self, source : SourceRequest) -> None:
        pass 
    
    @abstractmethod
    async def get_source(self, source_id: int) -> SourceResponse | None:
        pass 

    """
    @abstractmethod
    async def get_active_sources_from_db(self) -> list[SourceResponse]:
        pass
    """
    @abstractmethod
    async def get_sources(self, active : bool | None = None) -> list[SourceResponse] | None:
        pass

    @abstractmethod
    async def update_source(self, source_id: int, source: SourceUpdate) -> None:
        pass

    @abstractmethod
    async def delete_source(self, source_id: int) -> None:
        pass 