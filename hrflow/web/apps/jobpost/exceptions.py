


from hrflow.web.exceptions import DbRessourceNotFoundError, RepositoryError


class InvalidJobPostDataError(RepositoryError):
    "Invalid data while storing or updating a jobpost"

class JobPostNotFoundError(DbRessourceNotFoundError):
    "Unable to find jobpost error"

class InvalidApplicationError(RepositoryError):
    "Application saving invalid error"