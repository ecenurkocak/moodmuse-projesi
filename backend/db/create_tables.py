import asyncio
import logging

from .database import engine, Base
from backend.db.models import MoodEntry, Suggestion, User  # noqa

# Logger'ı yapılandır
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_database_tables() -> None:
    """
    SQLAlchemy modellerine dayanarak veritabanı tablolarını oluşturur.
    """
    logger.info("Veritabanı tabloları oluşturuluyor...")
    async with engine.begin() as conn:
        # Mevcut tabloları silmek için bu satırı etkinleştirebilirsiniz (dikkatli kullanın!)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Veritabanı tabloları başarıyla oluşturuldu.")


if __name__ == "__main__":
    # Betik doğrudan çalıştırıldığında asenkron fonksiyonu çalıştırır.
    # Proje ana dizinindeyken `python -m backend.db.create_tables` komutu ile çalıştırın.
    asyncio.run(create_database_tables()) 