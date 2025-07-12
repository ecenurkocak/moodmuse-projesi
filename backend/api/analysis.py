from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.auth import get_current_user
from backend.core.ai_service import get_ai_suggestions
from backend.db import crud
from backend.db.database import get_db
from backend.schemas import MoodEntry, MoodEntryCreate, SuggestionCreate, User


# İstek gövdesi için Pydantic modeli
class AnalysisRequest(BaseModel):
    text_input: str


router = APIRouter()


@router.post(
    "/analyze", response_model=MoodEntry, status_code=status.HTTP_201_CREATED
)
async def analyze_text_and_get_suggestions(
    request: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Kullanıcının metin girdisini analiz eder, öneriler üretir ve
    hem girdiyi hem de önerileri veritabanına kaydeder.
    """
    # 1. AI servisinden önerileri al
    ai_results = await get_ai_suggestions(request.text_input)

    # 2. MoodEntry oluştur ve veritabanına kaydet
    mood_entry_data = MoodEntryCreate(
        text_input=request.text_input, mood_label=str(ai_results["mood_label"])
    )
    db_mood_entry = await crud.create_mood_entry(
        db=db, mood_entry=mood_entry_data, user_id=current_user.id
    )

    # 3. Önerileri tek tek veritabanına kaydet
    # Renk paleti
    await crud.create_suggestion_for_mood_entry(
        db=db,
        suggestion=SuggestionCreate(
            suggestion_type="color", content=str(ai_results["color_palette"])
        ),
        mood_entry_id=db_mood_entry.id,  # type: ignore
    )
    # Spotify listesi
    await crud.create_suggestion_for_mood_entry(
        db=db,
        suggestion=SuggestionCreate(
            suggestion_type="music", content=str(ai_results["spotify_playlist"])
        ),
        mood_entry_id=db_mood_entry.id,  # type: ignore
    )
    # İlham verici söz
    await crud.create_suggestion_for_mood_entry(
        db=db,
        suggestion=SuggestionCreate(
            suggestion_type="quote", content=str(ai_results["inspirational_quote"])
        ),
        mood_entry_id=db_mood_entry.id,  # type: ignore
    )

    # SQLAlchemy'nin ilişkileri otomatik yüklemesi için refresh yetmeyebilir.
    # Bu nedenle, tam nesneyi ilişkileriyle birlikte yeniden sorguluyoruz.
    # Bu, en güncel ve eksiksiz veriyi döndürmeyi garanti eder.
    final_mood_entry = await crud.get_mood_entry_with_suggestions(
        db=db, mood_entry_id=db_mood_entry.id  # type: ignore
    )

    if not final_mood_entry:
        # Bu durumun normalde gerçekleşmemesi gerekir.
        # Ancak olası bir hataya karşı sistemi korumak için kontrol ekliyoruz.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve mood entry after creation.",
        )

    return final_mood_entry 