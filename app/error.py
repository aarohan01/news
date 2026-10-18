class AppError(Exception):
    pass

class IngestError(AppError):
    pass 

class ClientError(AppError):
    pass 