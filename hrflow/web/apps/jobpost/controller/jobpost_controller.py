from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi_router_controller import Controller
from dependency_injector.wiring import Provide, inject
from hrflow.web.apps.auth.auth_core import authenticated, authorized_with
from hrflow.web.apps.jobpost.exceptions import InvalidJobPostDataError, JobPostNotFoundError

from hrflow.web.apps.jobpost.schema import JobPostReq, JobPostRes
from hrflow.web.apps.jobpost.service.jobpost_service import JobPostService

router = APIRouter(prefix="/post",tags=["Jobpost controller"])
controller = Controller(router)


@controller.resource()
class JobPostController: 

    @inject
    def __init__(self, jobpost_service: JobPostService = Depends(Provide["jobpost_di_container.jobpost_service"])):
        self.jobpost_service = jobpost_service
    
    @controller.route.get("/{post_id}", response_model=JobPostRes)
    @authenticated
    async def get_jobpost(self, post_id:int, request:Request):
        """Get jobpost title, and body

        Args:
            post_id (int): post_id
            request (Request): injected

        Raises:
            HTTPException: 404 jobpost not found 

        Returns:
            JobPostRes: jobpost details
        """
        try:
            return self.jobpost_service.get_jobpost(post_id)
        except JobPostNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found error")

    @controller.route.get("/{user_id}", response_model=List[JobPostRes])
    @authenticated
    async def get_user_posts(self, user_id:int, request:Request):
        """Get specific user posts 

        Args:
            user_id (int): poster_id
            request (Request): injected

        Returns:
            List[JobPostRes]: List of jobposts details
        """
        return self.jobpost_service.get_user_posts(user_id=user_id)
    
    @controller.route.get("/", response_model=List[JobPostRes])
    @authenticated
    async def get_all_public_jobposts(self, request:Request):
        """get all public jobposts

        Args:
            request (Request): Injected

        Returns:
            List[JobPosts]: list of jobposts
        """
        return self.jobpost_service.get_all_public_jobposts()

    @controller.route.post("/{user_id}", status_code=status.HTTP_201_CREATED, response_model=JobPostRes)
    @inject
    @authorized_with(Provide['auth_di_container.user_owner_privilege'])
    async def create_jobpost(self,user_id:int, jobpost:JobPostReq, request:Request):
        """Creast a job post

        Args:
            user_id (int): the job offer poster
            jobpost (JobPostReq): Jobpost details
            request (Request): injected

        Raises:
            HTTPException: 400 in case of joboffer invalid cause of integrity errors

        Returns:
            JobPostRes: jobpost details with database id 
        """
        try:
            return self.jobpost_service.create_jobpost(user_id = user_id, jobpost = jobpost)
        except InvalidJobPostDataError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job post data")
        
    @controller.route.put("/{post_id}", response_model=JobPostRes)
    @inject
    @authorized_with(Provide['jobpost_di_container.jobpost_owner_privilege'])
    async def modify_jobpost(self, post_id:int, jobpost:JobPostReq, request:Request):
        """Update a jobpost offer

        Args:
            post_id (int): the actuall job post id
            jobpost (JobPostReq): the poster/owner of the job offer
            request (Request): injected

        Raises:
            HTTPException: 400 bad request due to integrity issues
            HTTPException: 404 incase of joboffer not found

        Returns:
            JobPostRes: Modified jobpost details
        """
        try:
            return self.jobpost_service.update_jobpost(jobpost=jobpost, post_id=post_id)
        except InvalidJobPostDataError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid job post data")
        except JobPostNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found error") 

    @controller.route.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
    @inject
    @authorized_with(Provide['jobpost_di_container.jobpost_owner_privilege'])
    async def delete_jobpost(self, post_id:int, request:Request):
        """delete a jobpost

        Args:
            post_id (int): joboffer id
            request (Request): injected

        Raises:
            HTTPException: 404 jobpost not found
        """
        try:
            self.jobpost_service.delete_jobpost(post_id)
        except JobPostNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found error")