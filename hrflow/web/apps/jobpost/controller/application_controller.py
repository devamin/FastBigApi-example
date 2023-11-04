from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_router_controller import Controller
from dependency_injector.wiring import Provide, inject
from hrflow.web.apps.auth.auth_core import authenticated, authorized_with
from hrflow.web.apps.jobpost.exceptions import InvalidApplicationError, JobPostNotFoundError

from hrflow.web.apps.jobpost.schema import ApplicationBodyReq, ApplicationRes
from hrflow.web.apps.jobpost.service.application_service import ApplicationService

router = APIRouter(prefix="/application",tags=["Application controller"])
controller = Controller(router)


@controller.resource()
class ApplicationController: 

    @inject
    def __init__(self, application_service: ApplicationService = Depends(Provide["jobpost_di_container.application_service"])):
        self.application_service = application_service
    
    @controller.route.post("/{post_id}/{user_id}", status_code=status.HTTP_202_ACCEPTED)
    @inject
    @authorized_with(Provide["auth_di_container.user_owner_privilege"])
    async def apply_for_ajobpost(self, user_id:int, post_id:int, application_body:Optional[ApplicationBodyReq], request:Request):
        try:
            self.application_service.apply_for_ajobpost(applicant_id=user_id, post_id=post_id, application_body=application_body)
        except InvalidApplicationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request applying for this role")
        except JobPostNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobpost not found") 

    @controller.route.get("/{post_id}", response_model=List[ApplicationRes])
    @inject
    @authorized_with(Provide['jobpost_di_container.jobpost_owner_privilege'])
    async def get_applications(self, post_id:int, request:Request):
        try:
            return self.application_service.get_applications(post_id=post_id)
        except JobPostNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobpost not found") 
    
        