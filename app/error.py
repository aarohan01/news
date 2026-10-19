# TODO : Enum type, internal, external 
# Rust Like -> return result or type of error and tag
# One convention 

class BaseError(Exception):
    pass

class IngestError(BaseError):
    pass 

class ClientError(BaseError):
    pass 