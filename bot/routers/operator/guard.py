# bot/routers/operator/guard.py
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.models.enums import UserRole

router = Router(name="operator_guard")

ALLOWED_TEXTS = {
    "О 🟢 Выйти на смену",
    "О ⬅️ В меню",
}

@router.message()
async def guard_messages(msg: Message, session, user):
    if user.role != UserRole.OPERATOR:
        return

    if msg.text in ALLOWED_TEXTS:
        return

    if await OperatorShiftDAO(session).get_active(user.id):
        return

    await msg.answer("❌ У вас нет активной смены")

@router.callback_query()
async def guard_callbacks(cb: CallbackQuery, session, user):
    if user.role != UserRole.OPERATOR:
        return

    if await OperatorShiftDAO(session).get_active(user.id):
        return

    try:
        await cb.answer("❌ У вас нет активной смены", show_alert=True)
    except TelegramBadRequest:
        pass
