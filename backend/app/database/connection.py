import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

USER = os.getenv("POSTGRES_USER", "postgres")
PASSWORD = quote_plus(os.getenv("POSTGRES_PASSWORD", "Hamand@95"))
# Use 127.0.0.1 explicitly to prevent IPv6 (::1) auth mismatch on Windows
SERVER = os.getenv("POSTGRES_SERVER", "127.0.0.1")
PORT = os.getenv("POSTGRES_PORT", "5432")
DB = os.getenv("POSTGRES_DB", "debugai_db")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Add Base for SQLAlchemy models to inherit from
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()