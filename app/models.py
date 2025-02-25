from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.orm import declarative_base, relationship
import enum

class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "student" or "teacher"

     # Relationship to Subscription
    subscription = relationship("Subscription", back_populates="user", uselist=False)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    plan = Column(String, nullable=False)  # "student" or "teacher"
    is_trial = Column(Boolean, default=True)  # True if in free trial
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

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False)
    last_accessed = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    lesson = relationship("Lesson")
