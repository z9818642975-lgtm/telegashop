# bot/services/catalog_service.py
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User


async def show_catalog(
    *,
    message: Message,
    session: AsyncSession | None,
    user: User | None,
):
    await message.answer("📦 Каталог")
