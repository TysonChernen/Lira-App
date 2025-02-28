from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from app.services.auth_service import hash_password, verify_password, create_access_token, get_current_user, require_role

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role  # Assign role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(db_user.id, db_user.email, db_user.role)


    return {"access_token": access_token, "token_type": "bearer"}



# ✅ Use role-based protection for teachers
@router.get("/teacher-dashboard")
def teacher_dashboard(current_user: dict = Depends(require_role("teacher"))):
    return {"message": f"Welcome, {current_user['email']}! You are authorized as a teacher."}

# ✅ Use role-based protection for students
@router.get("/student-dashboard")
def student_dashboard(current_user: dict = Depends(require_role("student"))):
    return {"message": f"Welcome, {current_user['email']}! You are authorized as a student."}

# ✅ General protected route for any authenticated user
@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['email']}! You are logged in as a {current_user['role']}."}
