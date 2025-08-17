import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.db.database import Base, engine
from backend.api import auth

# Static dosyalar için dizin oluştur
os.makedirs("static/profile_images", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama başlangıcında
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Veritabanı tabloları kontrol edildi ve oluşturuldu.")
    yield
    # Uygulama kapandığında burası çalışır (gerekirse)

app = FastAPI(
    title="MoodMuse API",
    description="API for mood analysis and suggestions.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS (Cross-Origin Resource Sharing) ayarları
origins = [
    "http://localhost:3000",  # Frontend'in adresi
    "http://127.0.0.1:3000", # Alternatif localhost adresi
    "http://localhost:3001",  # Next.js'in fallback portu
    "http://127.0.0.1:3001",
    "http://192.168.1.186:3000", # Yerel ağdaki erişim için eklendi
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Dosyaları Sunma
app.mount("/static", StaticFiles(directory="static"), name="static")


# API Rotalarını Dahil Et
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to MoodMuse API"}
