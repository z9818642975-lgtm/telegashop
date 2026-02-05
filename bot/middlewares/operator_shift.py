# bot/middlewares/operator_shift.py
from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest

from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.models.enums import UserRole


class OperatorShiftMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = data.get("user")
        session = data.get("session")

        if not user or user.role != UserRole.OPERATOR:
            return await handler(event, data)

        dao = OperatorShiftDAO(session)
        shift = await dao.get_active(user.tg_id)

        if shift:
            return await handler(event, data)

        try:
            if hasattr(event, "answer"):
                await event.answer("❌ У вас нет активной смены", show_alert=True)
        except TelegramBadRequest:
            pass

        return  # ⛔ стоп
