from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

router = Router(name="stub_handlers")


@router.callback_query()
async def stub_any_callback(
    cb: CallbackQuery,
    session: AsyncSession,
):
    await cb.answer("⏳ В разработке")
