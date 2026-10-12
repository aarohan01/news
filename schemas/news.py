from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ArticleRequest(BaseModel):

    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    source :str = Field(min_length=1)
    summary: str | None = None
    published: datetime | None = None
    guid: str | None = None


class ArticleResponse(BaseModel):

    id : int = Field(ge=0)
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    source :str = Field(min_length=1)
    summary: str | None = None
    published: datetime | None = None
    guid: str | None = None

    model_config = ConfigDict(from_attributes=True)