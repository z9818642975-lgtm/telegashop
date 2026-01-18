from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.models.user import User
from bot.services.catalog_service import show_catalog

router = Router(name="client_back")


@router.callback_query(F.data == CB.BACK_CATALOG)
async def back_to_catalog(
    cb: CallbackQuery,
    *,
    session: AsyncSession,
    user: User,
):
    await show_catalog(
        message=cb.message,
        session=session,
        user=user,
    )

