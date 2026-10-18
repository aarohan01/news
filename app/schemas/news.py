from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ArticleRequest(BaseModel):

    '''
    Validate the articles created from RSS entries according to our app
    '''
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    source_id : int = Field(ge=1)
    summary: str | None = None
    published: datetime | None = None
    guid: str | None = None


class ArticleResponse(BaseModel):

    '''
    Validate the articles as a response to display
    '''
    id : int = Field(ge=0)
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    source_id : int = Field(ge=1)
    summary: str | None = None
    published: datetime | None = None
    guid: str | None = None

    model_config = ConfigDict(from_attributes=True)