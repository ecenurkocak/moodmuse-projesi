import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


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


class SuggestionResponse(SuggestionBase):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


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


class MoodEntryResponse(MoodEntryBase):
    id: int
    created_at: datetime.datetime
    suggestions: List[SuggestionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class MoodEntry(MoodEntryBase):
    id: int
    created_at: datetime.datetime
    user_id: int
    suggestions: List[Suggestion] = []

    model_config = ConfigDict(from_attributes=True)


class HistoryResponse(BaseModel):
    total_entries: int
    page: int
    limit: int
    data: list[MoodEntryResponse]


class AnalysisRequest(BaseModel):
    text_input: str = Field(
        ...,
        description="The text input for which analysis is requested.",
    )


class AnalysisResponse(BaseModel):
    color_palette: list[str]
    spotify_playlist: str
    inspirational_quote: str


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
    

class UserResponse(UserBase):
    """Kullanıcı oluşturulduğunda veya getirildiğinde döndürülecek, hassas olmayan verileri içeren model."""
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True) 