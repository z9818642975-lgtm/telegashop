from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from bot.db.engine import engine

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

