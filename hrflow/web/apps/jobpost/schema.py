

from pydantic import BaseModel


class JobPostReq(BaseModel):
    title:str
    body:str

class JobPostRes(JobPostReq):
    id:int
    poster_username:str

class ApplicationBodyReq(BaseModel):
    cover_letter:str

class ApplicationRes(BaseModel):
    post_id:int
    applicant_id:int
    application_body:ApplicationBodyReq
