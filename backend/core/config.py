import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Projenin ana dizinini (bu dosyanın iki üst dizini) bul
# backend/core/config.py -> backend/ -> capstone/
env_path = Path(__file__).parent.parent.parent / ".env"

# Eğer projenin ana dizininde .env yoksa, backend dizinine bak
# Bu, dağıtım (deployment) senaryoları için esneklik sağlar
if not os.path.exists(env_path):
    env_path = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    """
    Uygulama ayarlarını .env dosyasından yükler.
    """
    PROJECT_NAME: str = "MoodMuse"
    # Eğer .env dosyasında DATABASE_URL tanımlanmamışsa, varsayılan olarak bir sqlite veritabanı kullan.
    DATABASE_URL: str = f"sqlite+aiosqlite:///{Path(__file__).parent.parent.parent / 'moodmuse.db'}"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GOOGLE_API_KEY: str
    HUGGING_FACE_API_KEY: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    model_config = SettingsConfigDict(
        env_file=str(env_path),  # pathlib.Path nesnesini string'e çevir
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()  # type: ignore 