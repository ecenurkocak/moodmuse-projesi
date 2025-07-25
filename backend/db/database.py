from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# ..core.config'den gelen settings'i import ediyoruz.
# Bu, config.py dosyasının bir üst dizindeki 'core' klasöründe olduğunu varsayar.
from ..core.config import settings

DATABASE_URL = settings.DATABASE_URL

# Veritabanı motorunu oluştur. `echo=True` geliştirme aşamasında
# çalıştırılan SQL sorgularını konsola basar, bu da hata ayıklama için kullanışlıdır.
# connect_args={"check_same_thread": False} sadece SQLite için gereklidir.
engine = create_async_engine(DATABASE_URL, echo=True)

# Asenkron oturumlar oluşturmak için bir fabrika (sessionmaker) tanımla.
# expire_on_commit=False, oturum kapatıldıktan sonra bile
# nesnelere erişimi sürdürmemizi sağlar.
AsyncSessionFactory = async_sessionmaker(
    bind=engine, 
    autoflush=False, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# Veritabanı modellerimiz için temel sınıf.
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Veritabanı oturumu için bir dependency.
    Her istekte yeni bir oturum açar ve istek bitince kapatır.
    """
    async with AsyncSessionFactory() as session:
        yield session 