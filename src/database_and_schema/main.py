from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, schemas, crud
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, get_current_user, require_role
from app.utils import verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Hiring System API",
    description="Backend for resume matching, job posting, job applications, and AI scoring.",
    version="1.0.0",
    debug=True
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# USERS
# ----------------------
@app.post("/users", response_model=schemas.UserOut, tags=["Users"], summary="Register new user", description="Register a new user (job_seeker or employer)")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/me", response_model=schemas.UserOut, tags=["Users"], summary="Get current user", description="Returns the currently logged-in user's profile")
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    return current_user

# ----------------------
# RESUMES
# ----------------------
@app.post("/resumes", response_model=schemas.ResumeOut, tags=["Resumes"], summary="Add resume", description="Add a resume (only for job seekers)")
def add_resume(
    resume: schemas.ResumeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("job_seeker"))
):
    return crud.create_resume(db, resume)

@app.get("/resumes/search", response_model=list[schemas.ResumeOut], tags=["Resumes"], summary="Search resumes", description="Search resumes by keyword using full-text search")
def resume_search(q: str, db: Session = Depends(get_db)):
    return crud.search_resumes(db, q)

@app.get("/resumes/{resume_id}", response_model=schemas.ResumeOut, tags=["Resumes"], summary="Get resume by ID", description="Retrieve a resume using its unique ID")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    return crud.get_resume_by_id(db, resume_id)

# ----------------------
# JOBS
# ----------------------
@app.post("/jobs", response_model=schemas.JobOut, tags=["Jobs"], summary="Post a job", description="Post a new job (only for employers)")
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("employer"))
):
    return crud.create_job(db, job)

@app.get("/jobs", response_model=list[schemas.JobOut], tags=["Jobs"], summary="List jobs", description="Get a list of all available jobs")
def list_jobs(db: Session = Depends(get_db)):
    return crud.get_all_jobs(db)

@app.get("/jobs/{job_id}/applications", response_model=list[schemas.JobApplicationOut], tags=["Applications"], summary="Applications for a job", description="Get all applications submitted to a specific job")
def get_applications_by_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_applications_by_job(db, job_id)

# ----------------------
# APPLICATIONS
# ----------------------
@app.post("/apply", response_model=schemas.JobApplicationOut, tags=["Applications"], summary="Apply to a job", description="Submit a resume to a job using resume_id and job_id")
def apply_to_job(
    application: schemas.JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("job_seeker"))
):
    return crud.create_application(db, application)

@app.get("/applications", response_model=list[schemas.JobApplicationOut], tags=["Applications"], summary="List all applications", description="List all job applications (admin/debug only)")
def list_applications(db: Session = Depends(get_db)):
    return crud.get_all_applications(db)

@app.get("/applications/by-user/{user_id}", response_model=list[schemas.JobApplicationOut], tags=["Applications"], summary="User's job applications", description="List all job applications submitted by a specific user")
def get_applications_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_applications_by_user(db, user_id)

# ----------------------
# LOGIN
# ----------------------
@app.post("/login", response_model=schemas.Token, tags=["Auth"], summary="Login", description="Login with email and password to receive an access token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}
