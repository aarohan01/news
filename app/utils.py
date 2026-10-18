import json 
import asyncio
from time import struct_time
from datetime import datetime

def pretty_print(article, length = None):

    '''
    Print json in pretty print format 
    '''
    if length :
        print(json.dumps(article,indent=2)[:length])
    else:
        print(json.dumps(article,indent=2))



def run_async(func, *args, **kwargs):

    '''
    Return the async functions wrapped in asyncio so that they can be run directly and tested 
    Does't run them in async format 
    '''
    return asyncio.run(func(*args,**kwargs))



def time_struct_to_datetime( stime : struct_time ) -> datetime:

    return datetime(*stime[:6])
    