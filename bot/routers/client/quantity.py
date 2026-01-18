from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.dao.order_items import OrderItemDAO
from bot.dao.products_dao import ProductsDAO
from bot.routers.client.catalog import render_catalog

router = Router(name="client_quantity")


@router.callback_query(F.data.startswith("qty:"))
async def select_quantity(
    cb: CallbackQuery,
    session: AsyncSession,
    user,
):
    """
    Callback format:
        qty:{product_id}:{qty}
    """

    # ---------- parse ----------
    try:
        _, product_id, qty = cb.data.split(":")
        product_id = int(product_id)
        qty = int(qty)
    except (ValueError, AttributeError):
        await cb.answer("Ошибка выбора количества", show_alert=True)
        return

    if qty <= 0:
        await cb.answer("Некорректное количество", show_alert=True)
        return

    # ---------- product ----------
    product = await ProductsDAO(session).get_by_id(product_id)
    if not product:
        await cb.answer("Товар не найден", show_alert=True)
        return

    # ---------- cart ----------
    orders_dao = OrdersDAO(session)
    items_dao = OrderItemDAO(session)

    order = await orders_dao.get_or_create_cart(user.id)

    await items_dao.add_or_increment(
        order_id=order.id,
        product_id=product.id,
        qty=qty,
        price=product.price,
    )

    await session.commit()

    # ---------- UX ----------
    await cb.answer("Добавлено в корзину")

    # 🔑 АВТОВОЗВРАТ В КАТАЛОГ
    await render_catalog(cb.message, session)
