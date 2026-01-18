from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.routers.client.catalog import render_catalog
router = Router(name="client_back")


@router.callback_query(F.data == CB.BACK_CATALOG)
async def back_to_catalog(
    cb: CallbackQuery,
    session: AsyncSession,
):
    await render_catalog(cb, session)

