import logging

from typing import Callable
from hrflow.database.models.jobpost_model import JobPostModel
from hrflow.database.models.user_model import UserModel
from hrflow.web.apps.auth.exceptions import InteractionWithUnfoundRessourceError, UnAuthorizedError, UserOperationNotAuthorized
from hrflow.web.apps.base.base_privilege import BasePrivilege
from hrflow.web.exceptions import DbRessourceNotFoundError

logger = logging.getLogger(__name__)

class JobPostOwnerPrivilege(BasePrivilege):
    
    def __init__(self, ressource_provider: Callable):
        super().__init__(ressource_provider=ressource_provider)

    def check(self, requester: UserModel, jobpost: JobPostModel):
        if requester.id != jobpost.poster_id:
            raise UnAuthorizedError

    def __call__(self, requester: UserModel, post_id: int):
        try:
            ressource = self.ressource_provider(post_id)
        except DbRessourceNotFoundError:
            raise InteractionWithUnfoundRessourceError

        try:
            self.check(requester=requester, jobpost=ressource)
        except UnAuthorizedError:
            logger.warn(
                f"User with id {requester.id} failed permission {self.__class__.__name__} "
                f"regarding ressource of type {type(ressource).__name__} with id {ressource.id}"
            )
            raise UserOperationNotAuthorized