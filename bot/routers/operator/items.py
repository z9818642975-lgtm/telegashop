# bot/routers/operator/items.py
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import (
    OperatorCheckAcceptCB,
    OperatorCheckRejectCB,
    OperatorDeliverySentCB,
    OperatorItemCB,
)
from bot.dao.orders import OrdersDAO
from bot.filters.role import RoleFilter
from bot.keyboards.operator.items import (
    operator_item_actions_kb,
)

router = Router(name="operator_items")
router.message.filter(RoleFilter.operator())


@router.callback_query(OperatorItemCB.filter())
async def operator_item(cb: CallbackQuery, callback_data: OperatorItemCB, session: AsyncSession):
    order_item = await OrdersDAO(session).get_item(callback_data.order_item_id)
    if not order_item:
        await cb.answer("Позиция не найдена", show_alert=True)
        return

    await cb.message.edit_text(
        f"📦 <b>Позиция заказа</b>\n"
        f"Товар: {order_item.product_name}\n"
        f"Кол-во: {order_item.qty}\n"
        f"Статус: {order_item.status}",
        reply_markup=operator_item_actions_kb(order_item),
    )
    await cb.answer()


@router.callback_query(OperatorCheckAcceptCB.filter())
async def operator_check_accept(
    cb: CallbackQuery,
    callback_data: OperatorCheckAcceptCB,
    session: AsyncSession,
):
    order = await OrdersDAO(session).accept_check(callback_data.order_id)
    if not order:
        await cb.answer("Заказ не найден", show_alert=True)
        return

    await cb.message.edit_text("✅ Чек принят. Заказ в работе.")
    await cb.answer()


@router.callback_query(OperatorCheckRejectCB.filter())
async def operator_check_reject(
    cb: CallbackQuery,
    callback_data: OperatorCheckRejectCB,
    session: AsyncSession,
):
    order = await OrdersDAO(session).reject_check(callback_data.order_id)
    if not order:
        await cb.answer("Заказ не найден", show_alert=True)
        return

    await cb.message.edit_text("❌ Чек отклонён. Клиент уведомлён.")
    await cb.answer()


@router.callback_query(OperatorDeliverySentCB.filter())
async def operator_delivery_sent(
    cb: CallbackQuery,
    callback_data: OperatorDeliverySentCB,
    session: AsyncSession,
):
    await OrdersDAO(session).mark_delivery_sent(callback_data.order_id)
    await cb.answer("Доставка отмечена как отправленная")