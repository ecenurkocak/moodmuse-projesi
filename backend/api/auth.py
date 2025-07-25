import logging
import json
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import crud
from ..core.config import settings
from ..core.security import create_access_token, verify_password
from ..core.ai_service import get_ai_suggestions
from ..db.database import get_db
from ..db.models import MoodEntry, Suggestion  # Modelleri doğrudan import et
from ..schemas import (
    Token, TokenData, User, UserCreate, UserResponse, 
    HistoryResponse, AnalysisRequest, AnalysisResponse,
    MoodEntryCreate, SuggestionCreate, MoodEntryResponse
)

# Token'ın hangi URL'den alınacağını belirtir.
# Bu, Swagger UI'ın "Authorize" butonu için gereklidir.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter()

# Logger'ı yapılandır
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """
    JWT'yi çözer, kullanıcıyı bulur ve döndürür.
    Korumalı endpoint'ler için bir dependency olarak kullanılır.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    if token_data.username is None:
        raise credentials_exception

    user = await crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Kullanıcı girişi yapar ve JWT döndürür.
    """
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(
        form_data.password, str(user.hashed_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> User:
    """
    Yeni bir kullanıcı kaydı oluşturur.
    - Kullanıcı adı veya e-posta zaten varsa hata döndürür.
    - Başarılı olursa yeni kullanıcıyı döndürür.
    """
    db_user_by_username = await crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu kullanıcı adı zaten kullanılıyor.",
        )
    
    db_user_by_email = await crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu e-posta adresi zaten kayıtlı.",
        )
        
    new_user = await crud.create_user(db=db, user=user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
async def analyze_text_and_get_suggestions(
    request: AnalysisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. AI servisinden sonuçları al
    ai_results = await get_ai_suggestions(request.text_input)

    # 2. MoodEntry ve Suggestion nesnelerini bellekte oluştur ve birbirine bağla
    db_mood_entry = MoodEntry(
        text_input=request.text_input,
        mood_label=str(ai_results["mood_label"]),
        user_id=current_user.id
    )
    
    suggestions = [
        Suggestion(
            suggestion_type="color",
            content=json.dumps(ai_results["color_palette"]),
        ),
        Suggestion(
            suggestion_type="music", content=ai_results["spotify_playlist"]
        ),
        Suggestion(
            suggestion_type="quote", content=ai_results["inspirational_quote"]
        ),
    ]
    db_mood_entry.suggestions.extend(suggestions)

    # 3. Ana nesneyi session'a ekle (ilişkili nesneler cascade ile eklenecek)
    db.add(db_mood_entry)
    
    # 4. Tüm işlemleri tek seferde commit et
    await db.commit()

    # 5. Başarılı yanıtı döndür
    return AnalysisResponse(
        color_palette=ai_results["color_palette"],
        spotify_playlist=ai_results["spotify_playlist"],
        inspirational_quote=ai_results["inspirational_quote"],
    )

@router.get(
    "/history",
    response_model=HistoryResponse,
)
async def get_user_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    limit: int = Query(9, ge=1, le=100, description="Sayfa başına girdi sayısı"),
):
    skip = (page - 1) * limit
    db_mood_entries = await crud.get_mood_entries_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    total_entries = await crud.count_mood_entries_by_user(db, user_id=current_user.id)
    
    # SQLAlchemy nesnelerini Pydantic modellerine manuel olarak dönüştür
    history_data = [MoodEntryResponse.model_validate(entry) for entry in db_mood_entries]

    return HistoryResponse(
        total_entries=total_entries,
        page=page,
        limit=limit,
        data=history_data,
    )

@router.delete("/history/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood_entry(
    entry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mood_entry = await crud.get_mood_entry_by_id(db, mood_entry_id=entry_id)
    if not mood_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Girdi bulunamadı."
        )
    if mood_entry.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu işlemi yapma yetkiniz yok.",
        )
    await crud.delete_mood_entry_by_id(db, mood_entry=mood_entry)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 