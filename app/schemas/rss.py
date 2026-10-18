from pydantic import BaseModel,Field, ConfigDict
from time import struct_time



class RSSEntryResponse(BaseModel):

    '''
    Validate the RSS entries from the RSS Sources
    '''
    title: str = Field(min_length=1)
    link: str = Field(min_length=1)
    summary: str | None = None
    guid: str | None = None
    published_parsed: struct_time 

    model_config = ConfigDict(arbitrary_types_allowed=True)


    
