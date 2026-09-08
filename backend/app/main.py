from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

# Import engine, get_db, and Base directly from connection
from app.database.connection import engine, get_db, Base
import app.models  # Ensures all models and relationships are registered

# Import routers
from app.routes import auth, projects, tests

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DebugAI",
    description="AI-Powered Intelligent Bug Detection and Root-Cause Analysis System",
    version="1.0.0"
)

# Include API Routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tests.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to DebugAI",
        "status": "running"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status
    }