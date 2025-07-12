from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# ..core.config'den gelen settings'i import ediyoruz.
# Bu, config.py dosyasının bir üst dizindeki 'core' klasöründe olduğunu varsayar.
from ..core.config import settings

# Veritabanı motorunu oluştur. `echo=True` geliştirme aşamasında
# çalıştırılan SQL sorgularını konsola basar, bu da hata ayıklama için kullanışlıdır.
# connect_args={"check_same_thread": False} sadece SQLite için gereklidir.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

# Asenkron oturumlar oluşturmak için bir fabrika (sessionmaker) tanımla.
# expire_on_commit=False, oturum kapatıldıktan sonra bile
# nesnelere erişimi sürdürmemizi sağlar.
AsyncSessionFactory = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)

# Veritabanı modellerimiz için temel sınıf.
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency'si olarak veritabanı oturumu sağlar.
    İstek tamamlandıktan sonra oturumun her zaman kapatılmasını garanti eder.
    """
    async with AsyncSessionFactory() as session:
        yield session 