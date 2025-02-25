from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Lesson, Progress
from app.services.auth_service import get_current_user

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/continue-learning")
def continue_learning(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Find the last lesson the user accessed."""
    last_lesson = (
        db.query(Progress)
        .filter(Progress.user_id == current_user["id"])
        .order_by(Progress.last_accessed.desc())
        .first()
    )

    if not last_lesson:
        raise HTTPException(status_code=404, detail="No lessons started yet.")

    return {
        "lesson_id": last_lesson.lesson_id,
        "last_accessed": last_lesson.last_accessed,
    }

@router.get("/dashboard/choose-lesson")
def choose_lesson(category: str = None, level: int = None, db: Session = Depends(get_db)):
    """Retrieve available lessons by category or level."""
    query = db.query(Lesson)
    if category:
        query = query.filter(Lesson.category == category)
    if level:
        query = query.filter(Lesson.level == level)

    lessons = query.all()
    
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found.")

    return lessons

@router.get("/dashboard/view-progress")
def view_progress(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get a user's completed lessons and progress."""
    progress = db.query(Progress).filter(Progress.user_id == current_user["id"]).all()

    return {
        "completed_lessons": [
            {"lesson_id": p.lesson_id, "completed": p.completed, "last_accessed": p.last_accessed}
            for p in progress
        ]
    }

