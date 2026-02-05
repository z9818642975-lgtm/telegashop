from aiogram import Router
from aiogram.types import CallbackQuery

router = Router(name="debug")

@router.callback_query(lambda c: c.data == "test:ping")
async def test_ping(cb: CallbackQuery):
    await cb.answer("PING OK", show_alert=True)
