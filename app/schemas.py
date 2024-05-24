from pydantic import BaseModel
from datetime import datetime


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class LeadCreate(LeadBase):
    resume: str


class LeadUpdate(BaseModel):
    state: str


class Lead(LeadBase):
    id: int
    resume_path: str
    state: str
    created_at: datetime

    class Config:
        orm_mode = True
