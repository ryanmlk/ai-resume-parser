from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from database_and_schema import models, schemas
from database_and_schema.utils import hash_password
from sqlalchemy import text

# -------------------------------
# CREATE NEW USER
# -------------------------------
def create_user(db: Session, user: schemas.UserCreate):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# -------------------------------
# CREATE NEW RESUME
# -------------------------------
def create_resume(db: Session, resume: schemas.ResumeCreate):
    # Check if the user exists before adding resume
    user = db.query(models.User).filter(models.User.user_id == resume.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_resume = models.Resume(
        user_id=resume.user_id,
        title=resume.title,
        summary=resume.summary,
        resume_text=resume.resume_text,
        created_at=datetime.utcnow()
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

# -------------------------------
# GET RESUME
# -------------------------------
def get_resume_by_id(db: Session, resume_id: int):
    resume = db.query(models.Resume).filter(models.Resume.resume_id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

# -------------------------------
# CREATE APPLICATION
# -------------------------------
def create_application(db: Session, app_data: schemas.JobApplicationCreate):
    resume = db.query(models.Resume).filter(models.Resume.resume_id == app_data.resume_id).first()
    job = db.query(models.Job).filter(models.Job.job_id == app_data.job_id).first()

    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job not found")

    application = models.JobApplication(
        resume_id=app_data.resume_id,
        job_id=app_data.job_id,
        applied_at=datetime.utcnow(),
        status="submitted"
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


# -------------------------------
# GET APPLICATION
# -------------------------------
def get_all_applications(db: Session):
    return db.query(models.JobApplication).all()

def get_applications_by_user(db: Session, user_id: int):
    return (
        db.query(models.JobApplication)
        .join(models.Resume)
        .filter(models.Resume.user_id == user_id)
        .all()
    )
def get_applications_by_job(db: Session, job_id: int):
    return (
        db.query(models.JobApplication)
        .filter(models.JobApplication.job_id == job_id)
        .all()
    )



# -------------------------------
# CREATE JOB
# -------------------------------
def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(
        user_id=job.user_id,
        job_title=job.job_title,
        job_description=job.job_description,
        job_location=job.job_location,
        posted_at=datetime.utcnow()
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job



# -------------------------------
# GET JOB
# -------------------------------
def get_all_jobs(db: Session):
    return db.query(models.Job).all()

def search_resumes(db: Session, query: str):
    formatted_query = " & ".join(query.lower().split())

    return db.query(models.Resume).filter(
        text("resume_search @@ to_tsquery(:q)")
    ).params(q=formatted_query).all()
