from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_router_controller import Controller
from dependency_injector.wiring import Provide, inject
from hrflow.web.apps.auth.exceptions import UserAlreadyExistsError, UserInvalidCredentialsError, UserNotFoundError
from hrflow.web.apps.auth.schema import SignUpReq

from hrflow.web.apps.auth.service.auth_service import AuthService

router = APIRouter(tags=["Authentication"])
controller = Controller(router)


@controller.resource()
class AuthController: 

    @inject
    def __init__(self, auth_service: AuthService = Depends(Provide["auth_di_container.auth_service"])):
        self.auth_service = auth_service

    @controller.route.post("/login")
    async def login(self, user_creds: OAuth2PasswordRequestForm = Depends()):
        try:
            return self.auth_service.user_login(user_creds=user_creds)
        except UserNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trying to login with unregistred user")
        except UserInvalidCredentialsError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        
    @controller.route.post("/signup")
    async def signup(self, signup_request: SignUpReq):
        try:
            return self.auth_service.user_signup(signup_request=signup_request)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")