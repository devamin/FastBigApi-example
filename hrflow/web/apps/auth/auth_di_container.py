from dependency_injector import containers, providers
from passlib.context import CryptContext

from hrflow.web.apps.auth.auth_settings import AuthSettings
from hrflow.web.apps.auth.core.password_hasher import PasswordHasher
from hrflow.web.apps.auth.privileges.user_owner_privilege import UserOwnerPrivilege
from hrflow.web.apps.auth.repository.user_repository import UserRepository
from hrflow.web.apps.auth.service.auth_service import AuthService


class AuthDIContainer(containers.DeclarativeContainer):

    auth_settings = providers.Singleton(AuthSettings)

    crypt_context = providers.Singleton(CryptContext, schemes=["bcrypt"], deprecated="auto")

    password_hasher = providers.Singleton(PasswordHasher, crypt_context=crypt_context)

    user_repository = providers.Singleton(UserRepository)

    auth_service = providers.Singleton(
        AuthService,
        auth_settings=auth_settings,
        password_hasher=password_hasher,
        user_repository=user_repository
    )

    user_owner_privilege = providers.Singleton(
        UserOwnerPrivilege, ressource_provider = auth_service.provided.get_user_by_id
    )