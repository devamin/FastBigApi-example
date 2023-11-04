
from typing import List, Optional
from sqlalchemy.orm import Session
from hrflow.database.models.application_model import ApplicationModel
from hrflow.web.apps.jobpost.exceptions import InvalidApplicationError
from hrflow.web.apps.jobpost.repository.application_repository import ApplicationRepository
from hrflow.web.apps.jobpost.schema import ApplicationBodyReq, ApplicationRes
from hrflow.web.apps.jobpost.service.jobpost_service import JobPostService
from hrflow.web.core import inject_db_session


class ApplicationService:

    def __init__(self, application_repository:ApplicationRepository, jobpost_service:JobPostService):
        self.application_repository = application_repository
        self.jobpost_service = jobpost_service

    @inject_db_session
    def apply_for_ajobpost(
            self, 
            applicant_id:int, 
            post_id:int,
            session:Session, 
            application_body:Optional[ApplicationBodyReq]= None):
        jobpost = self.jobpost_service.get_jobpost_by_id(post_id,session=session)
        if jobpost.poster_id == applicant_id:
            raise InvalidApplicationError
        if any(applicant.id == applicant_id for applicant in jobpost.applicants):
            return
        application = ApplicationModel(
            applicant_id = applicant_id,
            jobpost_id=post_id, 
            cover_letter=application_body.cover_letter
        )
        self.application_repository.save_application(application, session=session)

    @inject_db_session
    def get_applications(self, post_id:int,session:Session) -> List[ApplicationRes]:
        applications = self.application_repository.get_applications(post_id=post_id, session=session)
        return [
            ApplicationRes(
                post_id=post_id,
                applicant_id=application.applicant_id,
                application_body=ApplicationBodyReq(
                    cover_letter=application.cover_letter
                )
            )
            for application in applications
        ]
