from typing import Optional
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import delete

from hrflow.database.models.jobpost_model import JobPostModel
from hrflow.web.apps.jobpost.exceptions import InvalidJobPostDataError, JobPostNotFoundError


class JobPostRepository:
    
    def save_jobpost(self, jobpost:JobPostModel, session:Session):
        try:
            session.add(jobpost)
            session.flush()
            session.refresh(jobpost)
        except IntegrityError:
            raise InvalidJobPostDataError
        return jobpost
    
    def get_jobpost_by_id(self, post_id:int, session:Session):
        try: 
            return session.query(JobPostModel).filter(JobPostModel.id == post_id).one()
        except NoResultFound:
            raise JobPostNotFoundError
    
    def delete_jobpost(self, post_id:int, session:Session):
        q = delete(JobPostModel).where(JobPostModel.id == post_id)
        session.execute(q)

    def get_user_posts(self, user_id:int, session:Session):
        return (
            session.query(JobPostModel).filter(JobPostModel.poster_id == user_id).all()
        )
    
    def get_all_public_jobposts(self, session:Session):
        return session.query(JobPostModel).all()