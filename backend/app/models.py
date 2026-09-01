#defining how data stored in postgresql(database tables)

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from .database import Base
import enum
from sqlalchemy import ForeignKey

class StatusEnum(str, enum.Enum):  # we allowed the application status 
    saved = "Saved"
    applied = "Applied"
    oa = "OA"
    interview = "Interview"
    offer = "Offer"
    rejected = "Rejected"
    withdrawn = "Withdrawn"

class PriorityEnum(str, enum.Enum):  # setting priorities
    high = "High"
    medium = "Medium"
    low = "Low"

class Application(Base):   # describing table using py, nd sqlalchemy translates that model into database operations.
    __tablename__ = "applications"  # table name

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    location = Column(String, nullable=True)
    job_url = Column(String, nullable=True)
    source = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.saved, nullable=False)  # taking status from StatusEnum class
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium)  # taking priority from PriorityEnum class
    salary = Column(String, nullable=True)
    resume_used = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

#################################
#  user --> user_id --> application --> applkcation_id --> ineterviewround 
# 1 to many relationship (one Application can have many InterviewRounds)


class RoundTypeEnum(str, enum.Enum):  # allowed types of interview rounds
    phone_screen = "Phone Screen"
    technical = "Technical"
    hr = "HR"
    system_design = "System Design"
    case = "Case"

class OutcomeEnum(str, enum.Enum):  # outcomes for an interview round
    passed = "Passed"
    failed = "Failed"
    pending = "Pending"

class InterviewRound(Base):   # defining a sqlalchemy model representing interview rounds table 
    __tablename__ = "interview_rounds"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)  # if the application table has id=1,2,3.. then this represents the id col of that application id ,that y we call we foreign key of InterviewRound table
    round_number = Column(Integer, nullable=False)
    round_type = Column(Enum(RoundTypeEnum), nullable=False) # this comes from RoundTypeEnum class 
    date = Column(DateTime(timezone=True), nullable=True)
    interviewer = Column(String, nullable=True)
    outcome = Column(Enum(OutcomeEnum), default=OutcomeEnum.pending)
    notes = Column(Text, nullable=True)

