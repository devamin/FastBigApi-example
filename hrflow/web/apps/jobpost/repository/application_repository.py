from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from hrflow.database.models.application_model import ApplicationModel
from hrflow.web.apps.jobpost.exceptions import InvalidApplicationError


class ApplicationRepository:
    
    def save_application(self,application:ApplicationModel, session:Session):
        try:
            session.add(application)
            session.flush()
            session.refresh(application)
        except IntegrityError:
            raise InvalidApplicationError

    def get_applications(self, post_id:int,session:Session) -> List[ApplicationModel]:
        return session.query(ApplicationModel).filter(ApplicationModel.jobpost_id == post_id).all()