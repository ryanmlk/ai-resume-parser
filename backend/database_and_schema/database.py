from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()
 
user = "dbadmin"
password = os.getenv("DATABASE_PASSWORD")  # Your actual password
host = "resume-boost-db.postgres.database.azure.com"
port = 5432
db = "postgres"

encoded_pw = quote_plus(password)

DATABASE_URL = f"postgresql://{user}:{encoded_pw}@{host}:{port}/{db}?sslmode=require"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    print("Creating a new database session...")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
