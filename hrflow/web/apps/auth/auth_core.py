import asyncio
import inspect
import logging
from functools import partial
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from hrflow.database.models.user_model import UserModel
from hrflow.web.apps.auth.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    RequestParamMissingFromAuthenticatedHandlerError,
    InteractionWithUnfoundRessourceError, 
    UnAuthorizedError
)
from hrflow.web.apps.auth.service.auth_service import AuthService
from hrflow.web.apps.base.base_privilege import BasePrivilege
from hrflow.web.exceptions import DbRessourceNotFoundError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


logger = logging.getLogger(__name__)


def get_token_or_401(request):
    try:
        authorization = request.headers["authorization"]
        return authorization.split(" ")[1]
    except (KeyError, IndexError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def partial_privilege_args_fill(requester: UserModel, privilege: BasePrivilege, **kwargs):
    privilege_kwargs = {"requester": requester}
    privilege_params = inspect.signature(privilege).parameters.keys()
    privilege_kwargs = {
        "requester": requester,
        **{key: kwargs[key] for key in privilege_params if key != "requester"},
    }
    return partial(privilege, **privilege_kwargs)


def check_if_request_is_endpoint_handler_param(handler):
    if "request" not in inspect.signature(handler).parameters:
        logger.error("Check that request:Request is included in this endpoint")
        raise RequestParamMissingFromAuthenticatedHandlerError


@inject
def get_requester(
    token: str,
    auth_service: AuthService = Depends(Provide["auth_di_container.auth_service"]),
):
    try:
        return auth_service.get_user_from_token(token)
    except ExpiredTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except DbRessourceNotFoundError:
        logger.critical("When you see me just cry, unfound user successfully authenticated")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def validate_privileges(privileges: List[BasePrivilege]):
    for privilege in privileges:
        try:
            privilege()
            return
        except InteractionWithUnfoundRessourceError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except UnAuthorizedError:
            continue
        except TypeError as te:
            logger.error(te)
            logger.error(type(privilege))
            raise
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def authenticated(func):
    async def authenticated_wrapper(
        *args,
        token: str = Depends(oauth2_scheme),
        **kwargs,
    ):
        requester_user = get_requester(token=token)
        params_values = inspect.signature(func).parameters.values()
        for p in params_values:
            if p.name == "requester":
                kwargs[p.name] = requester_user
                break

        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    check_if_request_is_endpoint_handler_param(func)
    inspect.signature(func).parameters.values()
    authenticated_wrapper.__signature__ = inspect.Signature(
        parameters=[
            *inspect.signature(func).parameters.values(),
            *filter(
                lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                inspect.signature(authenticated_wrapper).parameters.values(),
            ),
        ],
        return_annotation=inspect.signature(func).return_annotation,
    )
    authenticated_wrapper.__name__ = func.__name__
    authenticated_wrapper.__doc__ = func.__doc__
    return authenticated_wrapper


def authorized_with(*privileges: BasePrivilege):
    def authorized_with_wrapper(func):
        async def wrapper(*args, token: str = Depends(oauth2_scheme), **kwargs):
            requester = get_requester(token=token)
            auth_privilege_keywords = []
            privileges: List[BasePrivilege] = []
            for key in kwargs.keys():
                if "auth_privilege" in key:
                    auth_privilege_keywords.append(key)
            for privilege in auth_privilege_keywords:
                privilege = kwargs.pop(privilege)
                privilege = partial_privilege_args_fill(requester=requester, privilege=privilege, **kwargs)
                privileges.append(privilege)
            validate_privileges(privileges)
            if "requester" in inspect.signature(func).parameters.keys():
                kwargs["requester"] = requester
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, partial(func, *args, **kwargs))

        check_if_request_is_endpoint_handler_param(func)
        auth_privileges = [
            inspect.Parameter(
                name=f"auth_privilege_{idx}",
                default=Depends(privilege),
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
            for idx, privilege in enumerate(privileges)
        ]
        func_parameters = [v for k, v in inspect.signature(func).parameters.items() if k != "requester"]
        wrapper.__signature__ = inspect.Signature(
            parameters=[
                *func_parameters,
                *auth_privileges,
                *filter(
                    lambda p: (p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD))
                    and (p.name not in inspect.signature(func).parameters),
                    inspect.signature(wrapper).parameters.values(),
                ),
            ],
            return_annotation=inspect.signature(func).return_annotation,
        )
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return authorized_with_wrapper

