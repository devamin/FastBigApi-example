from datetime import datetime, timedelta
import logging
from typing import Any, Dict
from jose import ExpiredSignatureError, JWTError, jwt

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm
from hrflow.database.connection.sql_connection_manager import SQLConnectionManager
from hrflow.database.models.user_model import UserModel
from hrflow.web.apps.auth.auth_settings import AuthSettings
from hrflow.web.apps.auth.core.password_hasher import PasswordHasher
from hrflow.web.apps.auth.exceptions import ExpiredTokenError, InvalidTokenError, UserInvalidCredentialsError
from hrflow.web.apps.auth.repository.user_repository import UserRepository
from hrflow.web.apps.auth.schema import SignUpReq, UserWithTokenRes
from hrflow.web.core import inject_db_session

logger = logging.getLogger(__name__)

class AuthService:
    
    def __init__(self, 
                 user_repository:UserRepository, 
                 auth_settings:AuthSettings, 
                 password_hasher:PasswordHasher):
        self.user_repository = user_repository
        self.auth_settings = auth_settings 
        self.password_hasher = password_hasher

    @inject_db_session
    def get_user_by_id(self, user_id:int, session:Session)->UserModel:
        return self.user_repository.get_user_by_id(user_id=user_id, session=session)

    @inject_db_session
    def user_login(self, user_creds:OAuth2PasswordRequestForm, session:Session):
        user_model:UserModel = self.user_repository.get_user(username=user_creds.username, session=session)
        if not self.password_hasher.verfiy_password(user_creds.password,user_model.password):
            raise UserInvalidCredentialsError
        return self._generate_token_response(user=user_model)
    
    @inject_db_session
    def user_signup(self, signup_request:SignUpReq, session:Session) -> UserWithTokenRes:
        user = self.user_repository.create_user(username=signup_request.username, password=self.password_hasher.hash_password(signup_request.password), session=session)
        return self._generate_token_response(user)
    
    @inject_db_session
    def get_user_from_token(self,token:str, session:Session):
        token_payload = self._decode_access_token(token=token)
        user = self.user_repository.get_user(username=token_payload.get("username"), session=session)
        return user

    def _generate_token_response(self, user:UserModel):
        return UserWithTokenRes(
            id=user.id, username=user.username, access_token=self._create_access_token(user)
        )
        
    def _create_access_token(self, user:UserModel) -> str:
        content_to_encode = {"id": user.id, "username":user.username}
        expire = datetime.utcnow() + timedelta(minutes=self.auth_settings.access_token_expire_minutes)
        content_to_encode.update({"exp": expire})
        return jwt.encode(content_to_encode, self.auth_settings.secret_key, algorithm=self.auth_settings.algorithm)
    
    def _decode_access_token(self, token: str) -> Dict[str,Any]:
        try:
            payload = jwt.decode(token, self.auth_settings.secret_key, algorithms=[self.auth_settings.algorithm])
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except JWTError:
            logger.warning("Trying to authenticate with invalid token")
            raise InvalidTokenError
        return payload
    