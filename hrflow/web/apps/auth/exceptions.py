

from hrflow.web.exceptions import DbRessourceNotFoundError, RepositoryError, ServiceError


class UserNotFoundError(DbRessourceNotFoundError):
    "User not found error"

class UserAlreadyExistsError(RepositoryError):
    "User already exist error when someone tries to re-register with same username"

class AuthServiceError(ServiceError):
    "Main auth service error class"

class UserInvalidCredentialsError(AuthServiceError):
    "User invalid credentials error"

class ExpiredTokenError(AuthServiceError):
    "Token expired"

class InvalidTokenError(AuthServiceError):
    "Token invalid"

class RequestParamMissingFromAuthenticatedHandlerError(AuthServiceError):
    "Validate endpoint handler"

 
class UnAuthorizedError(AuthServiceError):
    pass

class InteractionWithUnfoundRessourceError(UnAuthorizedError):
    pass

class UserOperationNotAuthorized(UnAuthorizedError):
    pass