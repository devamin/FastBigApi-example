from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from hrflow.database.models.application_model import ApplicationModel
from hrflow.database.models.base_db_model import BaseDBModel
from hrflow.database.models.user_model import UserModel
from sqlalchemy.orm import relationship

class JobPostModel(BaseDBModel):
    id:Mapped[int] = Column(Integer, primary_key=True)
    title:Mapped[str] = Column(String(50), nullable=False)
    body:Mapped[str] = Column(Text, nullable=False)
    poster_id:Mapped[int] = Column(Integer, ForeignKey("UserModel.id"))
    poster:Mapped[UserModel] = relationship('UserModel', uselist=False)
    applicants:Mapped[List[UserModel]] = relationship('UserModel', secondary=ApplicationModel.__table__, lazy="select")
