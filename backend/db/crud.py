import logging
from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional

from backend.db.models import User, MoodEntry, Suggestion
from backend.schemas import UserCreate, MoodEntryCreate, SuggestionCreate, UserUpdate
from backend.core.security import get_password_hash

# Logger'ı yapılandır
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Verilen e-posta adresine sahip kullanıcıyı veritabanından bulur."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Verilen kullanıcı adına sahip kullanıcıyı veritabanından bulur."""
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Verilen ID'ye sahip kullanıcıyı veritabanından bulur."""
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Yeni bir kullanıcı oluşturur ve veritabanına ekler."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user_update: "UserUpdate") -> User | None:
    """Kullanıcının profil bilgilerini (kullanıcı adı, bio) günceller."""
    
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return None
        
    update_data = user_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
            
    # Commit ve refresh işlemleri artık bu fonksiyonu çağıran endpoint'te yapılacak.
    return db_user


async def update_user_profile_image_url(db: AsyncSession, user_id: int, image_url: str) -> User | None:
    """Kullanıcının profil fotoğrafı URL'sini günceller."""
    
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    
    if not db_user:
        return None
        
    db_user.profile_image_url = image_url
            
    # Commit ve refresh işlemleri artık bu fonksiyonu çağıran endpoint'te yapılacak.
    return db_user


async def create_mood_entry(
    db: AsyncSession, mood_entry: MoodEntryCreate, user_id: int, emoji: Optional[str] = None
) -> MoodEntry:
    """Yeni bir duygu girdisi oluşturur ve veritabanına kaydeder."""
    db_mood_entry = MoodEntry(
        **mood_entry.model_dump(),
        user_id=user_id,
        emoji=emoji # Emoji'yi ekle
    )
    db.add(db_mood_entry)
    return db_mood_entry


async def create_suggestion_for_mood_entry(
    db: AsyncSession, suggestion: SuggestionCreate, mood_entry_id: int
) -> Suggestion:
    """Bir duygu girdisine bağlı yeni bir öneri oluşturur."""
    db_suggestion = Suggestion(
        **suggestion.model_dump(),
        mood_entry_id=mood_entry_id,
    )
    db.add(db_suggestion)
    return db_suggestion


async def get_mood_entries_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10
) -> list[MoodEntry]:
    """Belirli bir kullanıcıya ait duygu girişlerini, ilişkili önerilerle birlikte ve sayfalama yaparak getirir."""
    result = await db.execute(
        select(MoodEntry)
        .options(selectinload(MoodEntry.suggestions))
        .filter(MoodEntry.user_id == user_id)
        .order_by(MoodEntry.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def count_mood_entries_by_user(db: AsyncSession, user_id: int) -> int:
    """Belirli bir kullanıcıya ait toplam duygu girdisi sayısını döndürür."""
    result = await db.execute(
        select(func.count(MoodEntry.id)).filter(MoodEntry.user_id == user_id)
    )
    count = result.scalar_one_or_none()
    return count if count is not None else 0


async def get_mood_entry_by_id(db: AsyncSession, mood_entry_id: int) -> MoodEntry | None:
    """ID'ye göre tek bir duygu girdisi getirir."""
    result = await db.execute(
        select(MoodEntry).filter(MoodEntry.id == mood_entry_id)
    )
    return result.scalars().first()


async def delete_mood_entry_by_id(db: AsyncSession, mood_entry: MoodEntry) -> None:
    """Verilen bir duygu girdisini ve ilişkili önerilerini siler."""
    # İlişkili önerileri sil (cascade delete olsaydı buna gerek kalmazdı)
    await db.execute(delete(Suggestion).where(Suggestion.mood_entry_id == mood_entry.id))
    
    # Ana girdiyi sil
    await db.delete(mood_entry)


async def add_reasoning_to_mood_entry(
    db: AsyncSession, mood_entry: MoodEntry, reasoning_text: str
) -> MoodEntry:
    """Bir duygu girdisine 'neden' metnini ekler veya günceller."""
    mood_entry.reasoning_text = reasoning_text
    db.add(mood_entry)
    return mood_entry


async def get_mood_entry_with_suggestions(
    db: AsyncSession, mood_entry_id: int
) -> MoodEntry | None:
    """
    Belirli bir duygu girdisini, ilişkili tüm önerileriyle birlikte getirir.
    """
    result = await db.execute(
        select(MoodEntry)
        .options(selectinload(MoodEntry.suggestions))
        .filter(MoodEntry.id == mood_entry_id)
    )
    return result.scalars().first() 