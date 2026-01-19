from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.order_items import OrderItemDAO
from bot.routers.client.catalog import render_catalog

router = Router(name="client_quantity")


@router.callback_query(F.data.startswith("client:item:qty:"))
async def select_quantity(
    cb: CallbackQuery,
    session: AsyncSession,
):
    """
    Callback format:
        client:item:qty:<order_item_id>:<qty>
    """

    # ============================
    # PARSE
    # ============================
    try:
        _, _, _, item_id, qty = cb.data.split(":")
        item_id = int(item_id)
        qty = int(qty)
    except (ValueError, AttributeError):
        await cb.answer("Ошибка выбора количества", show_alert=True)
        return

    if qty <= 0:
        await cb.answer("Некорректное количество", show_alert=True)
        return

    items = OrderItemDAO(session)

    item = await items.get_by_id(item_id=item_id)
    if not item:
        await cb.answer("Позиция не найдена", show_alert=True)
        return

    # ============================
    # SET QUANTITY (НЕ increment)
    # ============================
    item.qty = qty
    await session.commit()

    await cb.answer("Количество обновлено")

    # ============================
    # AUTO RETURN TO CATALOG
    # ============================
    await render_catalog(cb, session)
