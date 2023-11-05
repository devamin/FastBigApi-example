from sqlalchemy.orm import Mapped
from sqlalchemy import Column, ForeignKey, Integer, Text, UniqueConstraint
from hrflow.database.models.base_db_model import BaseDBModel


class ApplicationModel(BaseDBModel):
    __table_args__ = (UniqueConstraint('applicant_id', 'jobpost_id', name='_applicant_jobpost_uc'),)

    id:Mapped[int] = Column(Integer, primary_key=True)
    applicant_id:Mapped[int] = Column(Integer, ForeignKey("UserModel.id",  ondelete="CASCADE"))
    jobpost_id:Mapped[int] = Column(Integer, ForeignKey("JobPostModel.id", ondelete="CASCADE"))
    cover_letter:Mapped[str] = Column(Text, nullable= True)