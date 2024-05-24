from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base


# database model in ORM
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    resume_path = Column(String(50), nullable=False)
    state = Column(String(20), nullable=False, default="PENDING")
    created_at = Column(DateTime, default=func.now())
