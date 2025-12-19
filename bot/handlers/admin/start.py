from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.core.config import settings

router = Router()

def _is_admin(tg_id: int) -> bool:
    return tg_id in settings.ADMINS

@router.message(Command("admin"))
async def admin(m: Message):
    if not _is_admin(m.from_user.id):
        return
    await m.answer("Админ-режим. Команды: /health_check")
