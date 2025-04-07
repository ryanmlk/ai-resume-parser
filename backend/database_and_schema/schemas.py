from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# -------------------------------
# USER SCHEMAS
# -------------------------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # 'employer' or 'job_seeker'

class UserOut(BaseModel):
    user_id: int
    name: str
    email: str
    role: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

# -------------------------------
# RESUME SCHEMAS
# -------------------------------

class ResumeCreate(BaseModel):
    user_id: int
    title: Optional[str]
    summary: Optional[str]
    resume_text: str

class ResumeOut(BaseModel):
    resume_id: int
    user_id: int
    title: Optional[str]
    summary: Optional[str]
    resume_text: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

# -------------------------------
# APPLICATION SCHEMAS
# -------------------------------
class JobApplicationCreate(BaseModel):
    resume_id: int
    job_id: int

class JobApplicationOut(BaseModel):
    application_id: int
    resume_id: int
    job_id: int
    applied_at: datetime
    status: str

    model_config = {
        "from_attributes": True
    }

# -------------------------------
# JOB SCHEMAS
# -------------------------------
class JobCreate(BaseModel):
    user_id: int
    job_title: str
    job_description: str
    job_location: Optional[str] = None

class JobOut(BaseModel):
    job_id: int
    user_id: int
    job_title: str
    job_description: str
    job_location: Optional[str]
    posted_at: datetime

    model_config = {
        "from_attributes": True
    }


# -------------------------------
# LOGIN SCHEMAS
# -------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int
