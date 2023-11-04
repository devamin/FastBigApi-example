from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound, IntegrityError
from hrflow.database.models.user_model import UserModel
from hrflow.web.apps.auth.exceptions import UserAlreadyExistsError, UserNotFoundError

class UserRepository():

    def create_user(self, username:str, password:str, session:Session) -> UserModel:
        user = UserModel(username=username, password=password)
        session.add(user)
        try:
            session.flush()        
            return user
        except IntegrityError:
            raise UserAlreadyExistsError

    def get_user(self, username:str, session:Session) -> UserModel:
        try:
            return session.query(UserModel).filter(UserModel.username==username).one()
        except NoResultFound:
            raise UserNotFoundError
        
    def get_user_by_id(self, user_id:int, session:Session) -> UserModel:
        try:
            return session.query(UserModel).filter(UserModel.id==user_id).one()
        except NoResultFound:
            raise UserNotFoundError