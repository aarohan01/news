from pydantic import BaseModel, Field


class SourceResponse(BaseModel):

    '''
    Validate the sources from the DB
    '''
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    url: str = Field(min_length=5)
    active: bool