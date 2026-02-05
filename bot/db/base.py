from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from bot.config import settings  # ← ВАЖНО

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

class Base(DeclarativeBase):
    pass
