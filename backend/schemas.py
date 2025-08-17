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
    id: Optional[int] = None


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
    reasoning_text: Optional[str] = None
    emoji: Optional[str] = None # YENİ ALAN
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


class ReasoningCreate(BaseModel):
    reasoning_text: str = Field(..., max_length=1000)


class AnalysisRequest(BaseModel):
    text_input: str = Field(
        ...,
        description="The text input for which analysis is requested.",
    )
    emoji: Optional[str] = Field(None, max_length=10) # YENİ ALAN


class AnalysisResponse(BaseModel):
    mood_entry_id: int # Bu alan frontend için gerekli
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
    profile_image_url: Optional[str] = None
    mood_entries: List[MoodEntry] = []

    model_config = ConfigDict(from_attributes=True)
    

class UserResponse(UserBase):
    """Kullanıcı oluşturulduğunda veya getirildiğinde döndürülecek, hassas olmayan verileri içeren model."""
    id: int
    created_at: datetime.datetime
    profile_image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """Kullanıcı profilini güncellerken kullanılacak model. Alanlar opsiyoneldir."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    bio: Optional[str] = Field(None, max_length=300)