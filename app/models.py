from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
import enum

# ✅ Define User Roles as Enum
class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)  # ✅ Uses Enum for validation

    # Relationship to Subscription
    subscription = relationship("Subscription", back_populates="user", uselist=False)

    # ✅ Track user progress in lessons
    progress = relationship("Progress", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    plan = Column(Enum(UserRole), nullable=False)  # ✅ Match with role enum
    is_trial = Column(Boolean, default=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)  # End of trial or subscription

    # Relationship back to User
    user = relationship("User", back_populates="subscription")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Example: "Phonics", "Reading"
    level = Column(Integer, nullable=False)
    content = Column(String, nullable=False)  # Lesson content (or link to content)

    # ✅ Add progress tracking
    progress = relationship("Progress", back_populates="lesson")

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False)
    last_accessed = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
