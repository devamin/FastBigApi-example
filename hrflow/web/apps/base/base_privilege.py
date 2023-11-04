from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Union

from hrflow.database.models.base_db_model import BaseDBModel
from hrflow.database.models.user_model import UserModel


class BasePrivilege(ABC):
    def __init__(self, ressource_provider: Optional[Callable] = None):
        self.ressource_provider = ressource_provider

    @abstractmethod
    def check(self, requester: UserModel, resource: Union[BaseDBModel, Any]):
        """Verify if the requester has enough perivilige to interact with this ressource."""
        pass

    @abstractmethod
    def __call__(self, requester: UserModel):
        """Get your ressource and call the check previlege."""
        # self.check(requester)
        pass
