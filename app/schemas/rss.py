from pydantic import BaseModel,Field, ConfigDict
from time import struct_time



class ParseResponse(BaseModel):

    '''
    Parse response validation
    '''
    title: str = Field(min_length=1)
    link: str = Field(min_length=1)
    summary: str | None = None
    guid: str | None = None
    published_parsed: struct_time 

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SourceRead(BaseModel):

    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    url: str = Field(min_length=5)
    active: bool
    
