from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Date
from sqlalchemy.orm import relationship
from database_and_schema.database import Base
from datetime import datetime

# -------------------------------
# USER MODEL
# -------------------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # 'employer' or 'job_seeker'
    created_at = Column(DateTime, default=datetime.utcnow)
    jobs = relationship("Job", back_populates="user")


    resumes = relationship("Resume", back_populates="user")


# -------------------------------
# RESUME MODEL
# -------------------------------
class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String(255))
    summary = Column(Text)
    resume_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    applications = relationship("JobApplication", back_populates="resume")
    user = relationship("User", back_populates="resumes")


# -------------------------------
# JOB MODEL
# -------------------------------
class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    job_title = Column(String(255))
    job_description = Column(Text)
    job_location = Column(String(100))
    posted_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job")


# -------------------------------
# APPLICATION MODEL
# -------------------------------
class JobApplication(Base):
    __tablename__ = "job_applications"

    application_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    job_id = Column(Integer, ForeignKey("jobs.job_id"))
    applied_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="submitted")

    resume = relationship("Resume", back_populates="applications")
    job = relationship("Job", back_populates="applications")


class ResumeSkill(Base):
    __tablename__ = "resume_skills"
    skill_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    skill_name = Column(String, nullable=False)
    proficiency_level = Column(String)

class ResumeExperience(Base):
    __tablename__ = "resume_experience"
    exp_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    job_title = Column(String)
    company_name = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)

class ResumeEducation(Base):
    __tablename__ = "resume_education"
    edu_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    institution_name = Column(String)
    degree = Column(String)
    field_of_study = Column(String)
    start_year = Column(Integer)
    end_year = Column(Integer)

class ResumeFeedback(Base):
    __tablename__ = "resume_feedback"
    feedback_id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.resume_id"))
    score = Column(Integer)
    feedback_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)