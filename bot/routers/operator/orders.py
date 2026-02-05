# bot/routers/operator/orders.py
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import OperatorDeliverySentCB, OperatorReady
from bot.dao.orders_dao import OrdersDAO
from bot.db import async_session_maker
from bot.middlewares.db import DBSessionMiddleware

router = Router(name="operator_orders")
router.callback_query.middleware(DBSessionMiddleware(async_session_maker))


@router.callback_query(OperatorReady.filter())
async def operator_ready(
    cb: CallbackQuery,
    callback_data: OperatorReady,
    session: AsyncSession,
):
    await OrdersDAO(session).assign_operator(
        order_id=callback_data.order_id,
        operator_id=cb.from_user.id,
    )
    await cb.answer("✅ Заказ принят в работу")


@router.callback_query(OperatorDeliverySentCB.filter())
async def operator_delivery_sent(
    cb: CallbackQuery,
    callback_data: OperatorDeliverySentCB,
    session: AsyncSession,
):
    await OrdersDAO(session).mark_ready(
        order_id=callback_data.order_id,
        operator_id=cb.from_user.id,
    )
    await cb.answer("🚚 Отправка отмечена")