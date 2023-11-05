

class HRFlowError(Exception):
    "Main hrflow exception class"

class ServiceError(HRFlowError):
    "Main hrflow service exception class"

class ControllerError(HRFlowError):
    "Main hrflow controller exception class"

class RepositoryError(HRFlowError):
    "Main hrflow repository exception class"


class DbRessourceNotFoundError(RepositoryError):
    "Main class to trigger no database result"
