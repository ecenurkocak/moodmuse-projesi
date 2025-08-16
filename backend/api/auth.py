import logging
import json
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.db import crud
from backend.core.config import settings
from backend.core.security import create_access_token, verify_password
from backend.core.ai_service import get_ai_suggestions
from backend.db.database import get_db
from backend.db.models import MoodEntry, Suggestion
from backend.schemas import (
    Token, TokenData, User, UserCreate, UserResponse, 
    HistoryResponse, AnalysisRequest, AnalysisResponse,
    MoodEntryResponse, UserUpdate
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Token'dan kullanıcı ID'sini string olarak al
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        # ID'yi integer'a çevirmeyi dene
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            # Eğer çevirme başarısız olursa, token geçersizdir.
            raise credentials_exception
        
        token_data = TokenData(id=user_id)
        
    except JWTError:
        raise credentials_exception

    # Veritabanından kullanıcıyı ID ile getir.
    user = await crud.get_user_by_id(db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
        
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    logger.info(f"Login attempt for username: '{form_data.username}'")
    user = await crud.get_user_by_username(db, username=form_data.username)
    
    if not user:
        logger.warning(f"Login failed: User '{form_data.username}' not found in database.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"User '{form_data.username}' found in database. Verifying password.")
    
    if not verify_password(form_data.password, str(user.hashed_password)):
        logger.warning(f"Login failed: Password verification failed for user '{form_data.username}'.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info(f"Password verified for user '{form_data.username}'. Creating access token.")
    # Token'ı oluştururken `sub` alanını string'e çevirerek tutarlılık sağla
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> User:
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
    ai_results = await get_ai_suggestions(request.text_input)

    if "error" in ai_results:
        raise HTTPException(status_code=500, detail=ai_results["error"])

    db_mood_entry = MoodEntry(
        text_input=request.text_input,
        mood_label=ai_results.get("mood_label", "bilinmiyor"),
        user_id=current_user.id
    )
    
    suggestions = [
        Suggestion(
            suggestion_type="color",
            content=",".join(ai_results.get("color_palette", [])),
        ),
        Suggestion(
            suggestion_type="music", 
            content=ai_results.get("spotify_playlist"),
        ),
        Suggestion(
            suggestion_type="quote", 
            content=ai_results.get("inspirational_quote"),
        ),
    ]
    db_mood_entry.suggestions.extend(suggestions)

    db.add(db_mood_entry)
    await db.commit()

    return AnalysisResponse(
        color_palette=ai_results.get("color_palette"),
        spotify_playlist=ai_results.get("spotify_playlist"),
        inspirational_quote=ai_results.get("inspirational_quote"),
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

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Oturum açmış kullanıcının profilini günceller."""
    logger.info(f"Updating profile for user ID: {current_user.id}")

    # Yeni kullanıcı adının başka bir kullanıcı tarafından kullanılıp kullanılmadığını kontrol et
    if user_update.username and user_update.username != current_user.username:
        existing_user = await crud.get_user_by_username(db, username=user_update.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu kullanıcı adı zaten kullanılıyor.",
            )

    try:
        updated_user = await crud.update_user(db, user_id=current_user.id, user_update=user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
        
        await db.commit()
        await db.refresh(updated_user)
        
        logger.info(f"Successfully updated profile for user ID: {updated_user.id}")
        return updated_user
    except Exception as e:
        logger.error(f"Error during profile update commit for user ID {current_user.id}: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profil güncellenirken bir sunucu hatası oluştu.",
        )

@router.post("/users/me/upload-profile-image", response_model=UserResponse)
async def upload_profile_image(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Oturum açmış kullanıcının profil fotoğrafını yükler."""
    
    # Dosya türü kontrolü
    allowed_content_types = ["image/jpeg", "image/png", "image/gif"]
    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Geçersiz dosya türü. Sadece JPEG, PNG veya GIF yükleyebilirsiniz.",
        )
        
    # Dosya boyutu kontrolü (Örnek: 5MB)
    max_file_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Dosya boyutu çok büyük. Maksimum boyut {max_file_size / (1024*1024)}MB.",
        )

    upload_dir = "static/profile_images"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Güvenli bir dosya adı oluştur
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{current_user.id}_{current_user.username}{file_extension}"
    file_path = os.path.join(upload_dir, file_name)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
        
    image_url = f"/static/profile_images/{file_name}"
    
    try:
        updated_user = await crud.update_user_profile_image_url(
            db, user_id=current_user.id, image_url=image_url
        )
        
        if not updated_user:
            # Bu durum normalde yaşanmamalı çünkü kullanıcıyı zaten get_current_user ile bulduk
            raise HTTPException(status_code=500, detail="Kullanıcı güncelleme sırasında bulunamadı.")
            
        await db.commit()
        await db.refresh(updated_user)
        return updated_user
    except Exception as e:
        logger.error(f"Error during profile image update commit for user ID {current_user.id}: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profil fotoğrafı güncellenirken bir sunucu hatası oluştu.",
        )

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Oturum açmış olan kullanıcının bilgilerini döndürür."""
    return current_user
