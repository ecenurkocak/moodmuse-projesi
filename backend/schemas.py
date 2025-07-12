import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ==============================================================================
# Token Şemaları (Authentication)
# ==============================================================================
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ==============================================================================
# Suggestion Şemaları (İç-içe kullanılacağı için önce tanımlanmalı)
# ==============================================================================
class SuggestionBase(BaseModel):
    suggestion_type: str
    content: str


class SuggestionCreate(SuggestionBase):
    pass


class Suggestion(SuggestionBase):
    id: int
    created_at: datetime.datetime
    mood_entry_id: int

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# MoodEntry Şemaları
# ==============================================================================
class MoodEntryBase(BaseModel):
    text_input: str
    mood_label: str


class MoodEntryCreate(MoodEntryBase):
    pass


class MoodEntry(MoodEntryBase):
    id: int
    created_at: datetime.datetime
    user_id: int
    suggestions: List[Suggestion] = []

    model_config = ConfigDict(from_attributes=True)


# ==============================================================================
# User Şemaları
# ==============================================================================
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime.datetime
    mood_entries: List[MoodEntry] = []

    model_config = ConfigDict(from_attributes=True) 