# bot/routers/operator/checks.py
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_operator import OperatorCheckCB
from bot.dao.orders_dao import OrdersDAO
from bot.db import async_session_maker
from bot.middlewares.db import DBSessionMiddleware

router = Router(name="operator_checks")
router.callback_query.middleware(DBSessionMiddleware(async_session_maker))


@router.callback_query(OperatorCheckCB.filter())
async def operator_check_result(
    cb: CallbackQuery,
    callback_data: OperatorCheckCB,
    session: AsyncSession,
):
    if callback_data.result == "paid":
        await OrdersDAO(session).mark_paid(
            order_id=callback_data.order_id,
        )
        await cb.answer("✅ Оплата подтверждена")
    else:
        await cb.answer("❌ Оплата отклонена")

