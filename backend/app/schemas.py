# defining what data is allowed to enter and leave the api

from pydantic import BaseModel
from typing import Optional 
from datetime import datetime
from .models import StatusEnum, PriorityEnum, RoundTypeEnum, OutcomeEnum

class ApplicationCreate(BaseModel):  # describing what the client is allowed to send when creating a new application
    company: str
    role: str
    location: Optional[str] = None
    job_url: Optional[str] = None
    source: Optional[str] = None
    status: StatusEnum = StatusEnum.saved
    priority: PriorityEnum = PriorityEnum.medium
    salary: Optional[str] = None
    resume_used: Optional[str] = None
    notes: Optional[str] = None

class ApplicationOut(ApplicationCreate):  # describing what server sends to clients while inheriting ApplicationCreate
    id: int
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):   # for patch 
    company: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    job_url: Optional[str] = None
    source: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    salary: Optional[str] = None
    resume_used: Optional[str] = None
    notes: Optional[str] = None


class UserCreate(BaseModel):  # describing what the client is allowed to send when creating a user
    email:str
    password:str


class Token(BaseModel):  # response from the login endpoint.
    access_token:str
    token_type:str = "bearer"


class RoundCreate(BaseModel): # what client send when creating a interview round
    round_number: int
    round_type: RoundTypeEnum
    date: Optional[datetime] = None
    interviewer: Optional[str] = None
    outcome: OutcomeEnum = OutcomeEnum.pending
    notes: Optional[str] = None

class RoundUpdate(BaseModel): # client changes 
    round_number: Optional[int] = None
    round_type: Optional[RoundTypeEnum] = None
    date: Optional[datetime] = None
    interviewer: Optional[str] = None
    outcome: Optional[OutcomeEnum] = None
    notes: Optional[str] = None

class RoundOut(RoundCreate): 
    id:int
    application_id:int

    class Config:
        from_attributes = True
