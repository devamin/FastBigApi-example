import logging

from typing import Callable
from hrflow.database.models.user_model import UserModel
from hrflow.web.apps.auth.exceptions import InteractionWithUnfoundRessourceError, UnAuthorizedError, UserOperationNotAuthorized
from hrflow.web.apps.base.base_privilege import BasePrivilege
from hrflow.web.exceptions import DbRessourceNotFoundError

logger = logging.getLogger(__name__)

class UserOwnerPrivilege(BasePrivilege):
    
    def __init__(self, ressource_provider: Callable):
        super().__init__(ressource_provider=ressource_provider)

    def check(self, requester: UserModel, user_model: UserModel):
        if requester.id != user_model.id:
            raise UnAuthorizedError

    def __call__(self, requester: UserModel, user_id: int):
        try:
            ressource = self.ressource_provider(user_id)
        except DbRessourceNotFoundError:
            raise InteractionWithUnfoundRessourceError

        try:
            self.check(requester=requester, user_model=ressource)
        except UnAuthorizedError:
            logger.warn(
                f"User with id {requester.id} failed permission {self.__class__.__name__} "
                f"regarding ressource of type {type(ressource).__name__} with id {ressource.id}"
            )
            raise UserOperationNotAuthorized