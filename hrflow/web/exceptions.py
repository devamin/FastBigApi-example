

class HRFlowError(Exception):
    "Main hrflow exception class"

class ServiceError(HRFlowError):
    "Main hrflow service exception class"

class ControllerError(Exception):
    "Main hrflow controller exception class"

class RepositoryError(Exception):
    "Main hrflow repository exception class"


class DbRessourceNotFoundError(RepositoryError):
    pass
