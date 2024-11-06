from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String, index=True)
    weight = Column(Integer)
    height = Column(Integer)
