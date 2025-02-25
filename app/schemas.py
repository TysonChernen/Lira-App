from pydantic import BaseModel, EmailStr
from app.models import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole  # New field for specifying user role

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole  # Include role in response

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
