from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.orders_dao import OrdersDAO
from bot.routers.client.catalog import render_catalog

router = Router(name="client_quantity")


@router.callback_query(F.data.startswith("qty:"))
async def select_quantity(cb: CallbackQuery, session: AsyncSession):
    """
    qty:{product_id}:{qty}
    """
    try:
        _, product_id, qty = cb.data.split(":")
        product_id = int(product_id)
        qty = int(qty)
    except ValueError:
        await cb.answer("Ошибка выбора количества", show_alert=True)
        return

    if qty <= 0:
        await cb.answer("Некорректное количество", show_alert=True)
        return

    await OrdersDAO.add_item(
        session=session,
        client_id=cb.from_user.id,
        product_id=product_id,
        qty=qty,
    )
    await session.commit()

    await cb.answer("Добавлено в корзину")

    # 🔑 КАНОН: никаких новых сообщений, только возврат в каталог
    await render_catalog(cb, session)

