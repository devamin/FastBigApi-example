from typing import List, Optional
from sqlalchemy.orm import Session

from hrflow.database.models.jobpost_model import JobPostModel
from hrflow.web.apps.jobpost.repository.jobpost_repository import JobPostRepository
from hrflow.web.apps.jobpost.schema import JobPostReq, JobPostRes
from hrflow.web.core import inject_db_session


class JobPostService:

    def __init__(self, jobpost_repository:JobPostRepository):
        self.jobpost_repository = jobpost_repository

    @inject_db_session
    def get_jobpost_by_id(self, post_id:int, session:Session)-> JobPostModel:
        return self.jobpost_repository.get_jobpost_by_id(post_id=post_id, session=session)
    
    @inject_db_session
    def create_jobpost(self, user_id:int,jobpost:JobPostReq, session:Session)->JobPostRes:
        jobpost_model = JobPostModel(
            title = jobpost.title, 
            body = jobpost.body,
            poster_id=user_id
        )
        jobpost_model = self.jobpost_repository.save_jobpost(jobpost=jobpost_model, session=session)
        return JobPostRes(
            **{
                **jobpost_model.to_dict(),
               "poster_username":jobpost_model.poster.username}
        )

    @inject_db_session
    def update_jobpost(self, jobpost:JobPostReq, post_id:int, session:Session):
        jobpost_model = self.jobpost_repository.get_jobpost_by_id(post_id=post_id, session=session)
        jobpost_model.update_from_model(jobpost)
        return JobPostRes(
            **{
                **jobpost_model.to_dict(),
               "poster_username":jobpost_model.poster.username}
        )
    
    @inject_db_session
    def delete_jobpost(self, post_id:int, session:Session):
        self.jobpost_repository.delete_jobpost(post_id=post_id, session=session)

    @inject_db_session
    def get_jobpost(self, post_id:int, session:Session):
        jobpost_model = self.jobpost_repository.get_jobpost_by_id(post_id=post_id, session=session) 
        return JobPostRes(
            **{
                **jobpost_model.to_dict(),
               "poster_username":jobpost_model.poster.username}
        )
    
    @inject_db_session
    def get_user_posts(self, user_id:int, session:Session) -> List[JobPostRes]:
        return [
            JobPostRes(
            **{
                **jobpost_model.to_dict(),
               "poster_username":jobpost_model.poster.username}
            )
            for jobpost_model in self.jobpost_repository.get_user_posts(user_id=user_id, session=session)
        ]
    
    @inject_db_session
    def get_all_public_jobposts(self, session:Session)->List[JobPostRes]:
        return [
            JobPostRes(
            **{
                **jobpost_model.to_dict(),
               "poster_username":jobpost_model.poster.username}
            )
            for jobpost_model in self.jobpost_repository.get_all_public_jobposts(session=session)
        ]
        