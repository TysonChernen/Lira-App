from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.subscription_service import start_free_trial, upgrade_to_paid
from app.services.auth_service import get_current_user

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start-trial/{plan}")
def start_trial(plan: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if plan not in ["student", "teacher"]:
        raise HTTPException(status_code=400, detail="Invalid plan type")

    return start_free_trial(user_id=current_user["id"], plan=plan, db=db)

@router.post("/subscribe/{plan}")
def subscribe(plan: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if plan not in ["student", "teacher"]:
        raise HTTPException(status_code=400, detail="Invalid plan type")

    return upgrade_to_paid(user_id=current_user["id"], plan=plan, db=db)

