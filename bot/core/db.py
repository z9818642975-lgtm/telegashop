from __future__ import annotations
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from bot.core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
