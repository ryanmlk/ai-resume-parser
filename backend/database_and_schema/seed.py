from sqlalchemy.orm import Session
from database_and_schema.database import SessionLocal, engine
from database_and_schema import models
from utils import hash_password
from faker import Faker
import random

# Reset DB (optional)
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()
fake = Faker()

# === USERS ===
user_ids = []
for i in range(6):
    role = "job_seeker" if i < 3 else "employer"
    user = models.User(
        name=fake.name(),
        email=f"user{i}@example.com",
        password_hash=hash_password("password123"),
        role=role,
        created_at=fake.date_time_this_year()
    )
    db.add(user)
    db.flush()
    user_ids.append((user.user_id, role))

# === RESUMES ===
resume_ids = []
for user_id, role in user_ids:
    if role == "job_seeker":
        for _ in range(2):
            resume = models.Resume(
                user_id=user_id,
                title=fake.job(),
                summary=fake.sentence(),
                resume_text=" ".join(fake.words(12)),
                created_at=fake.date_time_this_year()
            )
            db.add(resume)
            db.flush()
            resume_ids.append(resume.resume_id)

            # === SKILLS ===
            for skill in random.sample(["Python", "Docker", "SQL", "AWS", "FastAPI", "React", "Kubernetes", "Git"], 4):
                db.add(models.ResumeSkill(
                    resume_id=resume.resume_id,
                    skill_name=skill,
                    proficiency_level=random.choice(["Beginner", "Intermediate", "Advanced"])
                ))

            # === EXPERIENCE ===
            for _ in range(2):
                db.add(models.ResumeExperience(
                    resume_id=resume.resume_id,
                    job_title=fake.job(),
                    company_name=fake.company(),
                    start_date=fake.date_between(start_date='-3y', end_date='-1y'),
                    end_date=fake.date_between(start_date='-1y', end_date='today'),
                    description=fake.text(max_nb_chars=200)
                ))

            # === EDUCATION ===
            db.add(models.ResumeEducation(
                resume_id=resume.resume_id,
                institution_name=fake.company() + " University",
                degree=random.choice(["B.Sc", "M.Sc", "B.Tech", "MBA"]),
                field_of_study=random.choice(["Computer Science", "AI", "Business", "Engineering"]),
                start_year=random.randint(2015, 2018),
                end_year=random.randint(2019, 2022)
            ))

# === JOBS ===
job_ids = []
for user_id, role in user_ids:
    if role == "employer":
        for _ in range(3):
            job = models.Job(
                user_id=user_id,
                job_title=fake.job(),
                job_description=fake.paragraph(nb_sentences=3),
                job_location=random.choice(["Remote", "On-site", "Hybrid"]),
                posted_at=fake.date_time_this_year()
            )
            db.add(job)
            db.flush()
            job_ids.append(job.job_id)

# === APPLICATIONS ===
statuses = ["pending", "reviewed", "rejected"]
for resume_id in random.sample(resume_ids, k=len(resume_ids)):
    db.add(models.JobApplication(
        resume_id=resume_id,
        job_id=random.choice(job_ids),
        applied_at=fake.date_time_this_month(),
        status=random.choice(statuses)
    ))

# === FEEDBACK ===
for resume_id in resume_ids:
    db.add(models.ResumeFeedback(
        resume_id=resume_id,
        score=random.randint(60, 95),
        feedback_text=fake.sentence(),
        created_at=fake.date_time_this_month()
    ))

db.commit()
db.close()
print("✅ Fully seeded: users, resumes, jobs, applications, skills, experience, education, feedback.")
