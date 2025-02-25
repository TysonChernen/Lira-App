from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from sqlalchemy.orm import declarative_base
import enum

class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.student)



