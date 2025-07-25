import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    mood_entries = relationship("MoodEntry", back_populates="owner", lazy="selectin")


class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    text_input = Column(Text, nullable=False)
    mood_label = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="mood_entries", lazy="selectin")
    suggestions = relationship(
        "Suggestion", back_populates="mood_entry", cascade="all, delete-orphan", lazy="selectin"
    )


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    suggestion_type = Column(String, nullable=False)  # 'color', 'music', 'quote'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    mood_entry_id = Column(Integer, ForeignKey("mood_entries.id"), nullable=False)

    mood_entry = relationship("MoodEntry", back_populates="suggestions", lazy="selectin") 