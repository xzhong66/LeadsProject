from typing import Optional

from pydantic import BaseModel
from datetime import datetime


# data models for request and response
class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    resume: str


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    state: str


class Lead(LeadBase):
    id: int
    state: str
    created_at: datetime

    class Config:
        orm_mode = True

