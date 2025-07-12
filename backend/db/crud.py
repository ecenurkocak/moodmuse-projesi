from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backend.core.security import get_password_hash
from backend.db.models import MoodEntry, Suggestion, User
from backend.schemas import MoodEntryCreate, SuggestionCreate, UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Verilen e-posta adresine sahip kullanıcıyı veritabanından bulur."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Verilen kullanıcı adına sahip kullanıcıyı veritabanından bulur."""
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """Yeni bir kullanıcı oluşturur ve veritabanına kaydeder."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_mood_entry(
    db: AsyncSession, mood_entry: MoodEntryCreate, user_id: int
) -> MoodEntry:
    """Yeni bir duygu girdisi oluşturur ve veritabanına kaydeder."""
    db_mood_entry = MoodEntry(
        **mood_entry.model_dump(),
        user_id=user_id,
    )
    db.add(db_mood_entry)
    await db.commit()
    await db.refresh(db_mood_entry)
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
    await db.commit()
    await db.refresh(db_suggestion)
    return db_suggestion


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