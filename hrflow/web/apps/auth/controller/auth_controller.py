from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi_router_controller import Controller
from dependency_injector.wiring import Provide, inject
from hrflow.web.apps.auth.exceptions import UserAlreadyExistsError, UserInvalidCredentialsError, UserNotFoundError
from hrflow.web.apps.auth.schema import SignUpReq, UserWithTokenRes

from hrflow.web.apps.auth.service.auth_service import AuthService

router = APIRouter(tags=["Authentication"])
controller = Controller(router)


@controller.resource()
class AuthController: 

    @inject
    def __init__(self, auth_service: AuthService = Depends(Provide["auth_di_container.auth_service"])):
        self.auth_service = auth_service

    @controller.route.post("/login", response_model=UserWithTokenRes)
    async def login(self, user_creds: OAuth2PasswordRequestForm = Depends()):
        """Login with username and password to get access token

        Args:
            user_creds (OAuth2PasswordRequestForm, optional): multi-data body for username and password

        Raises:
            HTTPException: 404 user unregistred 
            HTTPException: 403 invalid credentials

        Returns:
            UserWithTokenRes: user_id with access token
        """
        try:
            return self.auth_service.user_login(user_creds=user_creds)
        except UserNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trying to login with unregistred user")
        except UserInvalidCredentialsError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
        
    @controller.route.post("/signup", response_model=UserWithTokenRes)
    async def signup(self, signup_request: SignUpReq):
        """Create a user with username and password 

        Args:
            signup_request (SignUpReq): Signup with username password and password confirmation

        Raises:
            HTTPException: 403 username already exists

        Returns:
            UserWithTokenRe: user_id with access token and token type
        """
        try:
            return self.auth_service.user_signup(signup_request=signup_request)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")