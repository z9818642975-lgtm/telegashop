# bot/db/session.py

from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.base import engine

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
