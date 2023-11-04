from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String
from hrflow.database.models.base_db_model import BaseDBModel


class UserModel(BaseDBModel):
    id:Mapped[int] = Column(Integer, primary_key=True)
    username:Mapped[str] = Column(String(50), nullable=False, unique= True)
    
    password:Mapped[str] = Column(String(100), nullable=False)