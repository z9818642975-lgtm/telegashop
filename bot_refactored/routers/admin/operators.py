from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.constants.roles import ADMINS
from bot_refactored.app.admin.operators import (
    CreateOperatorUseCase,
    ArchiveOperatorUseCase,
)

router = Router(name="admin_operators")

def _is_admin(client_id: int) -> bool:
    return client_id in ADMINS

@router.message(F.text.startswith("/add_operator"))
async def add_operator(msg: Message, session: AsyncSession):
    if not _is_admin(msg.from_user.id):
        return
    telegram_id = int(msg.text.split()[-1])
    await CreateOperatorUseCase(telegram_id, session).execute()
    await msg.answer("Оператор добавлен")

@router.message(F.text.startswith("/archive_operator"))
async def archive_operator(msg: Message, session: AsyncSession):
    if not _is_admin(msg.from_user.id):
        return
    telegram_id = int(msg.text.split()[-1])
    await ArchiveOperatorUseCase(telegram_id, session).execute()
    await msg.answer("Оператор архивирован")

