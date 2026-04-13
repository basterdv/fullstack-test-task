from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs,AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from src.core.config import settings

# Создаем асинхронный движок
engine = create_async_engine(
    settings.DB_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

# Фабрика асинхронных сессий
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


# Dependency для внедрения сессии в эндпоинты FastAPI
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
