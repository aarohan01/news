from pydantic import BaseModel, Field


class SourceResponse(BaseModel):

    '''
    Validate the sources from the DB
    '''
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    url: str = Field(min_length=5)
    active: bool


class SourceRequest(BaseModel):

    '''
    Add the sources to the DB
    '''
    name: str = Field(min_length=1)
    url: str = Field(min_length=5)
    active: bool | None

class SourceUpdate(BaseModel):

    '''
    Update the source in DB
    '''
    name: str | None = Field(default=None, min_length=1)
    url: str | None = Field(default=None, min_length=5)
    active: bool | None = None

