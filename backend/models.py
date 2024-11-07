from sqlalchemy import Column, Integer, String
from .database import Base

class UserMessage(Base):
    __tablename__ = "user_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    username = Column(String, index=True)
    text = Column(String)
