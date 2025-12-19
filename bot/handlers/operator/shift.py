from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.db import get_session
from bot.services.operator_service import OperatorService

router = Router()

@router.message(Command("shift_start"))
async def shift_start(m: Message, session: AsyncSession = get_session()):
    address = m.text.replace("/shift_start", "").strip()
    if not address:
        await m.answer("Укажи адрес: /shift_start Ленина 12")
        return
    shift = await OperatorService(session).start_shift(m.from_user.id, address)
    await m.answer(f"✅ Смена начата. Адрес: {address} (shift_id={shift.id})")

@router.message(Command("shift_end"))
async def shift_end(m: Message, session: AsyncSession = get_session()):
    await OperatorService(session).end_shift(m.from_user.id)
    await m.answer("⏹ Смена завершена")
