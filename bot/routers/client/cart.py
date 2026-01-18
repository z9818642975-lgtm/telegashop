from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.dao.order_items import OrderItemDAO
from bot.keyboards.client.cart import cart_inline_kb
from bot.routers.client.catalog import render_catalog

router = Router(name="client_cart")


@router.callback_query(F.data == CB.CART_OPEN)
async def open_cart(cb: CallbackQuery, session: AsyncSession, user):
    await render_cart(cb, session, user)


async def render_cart(cb: CallbackQuery, session: AsyncSession, user):
    orders = OrdersDAO(session)
    order = await orders.get_cart(user.id)

    if not order or not order.items:
        await cb.message.edit_text(
            "🧺 <b>Корзина пуста</b>\n\nВыберите товары в каталоге.",
            reply_markup=None,
        )
        return

    total = sum(item.qty * item.price for item in order.items)

    lines: list[str] = ["🧺 <b>Корзина</b>\n"]
    for item in order.items:
        lines.append(
            f"• {item.product.title} × {item.qty} = {item.qty * item.price} ₽"
        )

    lines.append(f"\n<b>Итого:</b> {total} ₽")

    await cb.message.edit_text(
        "\n".join(lines),
        reply_markup=cart_inline_kb(order.items),
    )


# ❌ УДАЛЕНИЕ КОНКРЕТНОГО ТОВАРА
@router.callback_query(F.data.startswith("item:remove:"))
async def remove_item(cb: CallbackQuery, session: AsyncSession, user):
    item_id = int(cb.data.split(":")[2])

    items = OrderItemDAO(session)
    item = await items.get_by_id(item_id=item_id)

    if item:
        await session.delete(item)
        await session.commit()

    await render_cart(cb, session, user)


# 🔢 УСТАНОВКА КОЛИЧЕСТВА (НЕ СУММИРОВАНИЕ)
@router.callback_query(F.data.startswith("item:qty:"))
async def set_item_qty(cb: CallbackQuery, session: AsyncSession, user):
    _, _, item_id, qty = cb.data.split(":")
    item_id = int(item_id)
    qty = int(qty)

    items = OrderItemDAO(session)
    item = await items.get_by_id(item_id=item_id)

    if item:
        # 🔴 КРИТИЧНО: КОЛИЧЕСТВО ПОЛНОСТЬЮ ЗАМЕНЯЕТСЯ
        item.qty = qty
        await session.commit()

    await render_cart(cb, session, user)


@router.callback_query(F.data == CB.CART_CLEAR)
async def clear_cart(cb: CallbackQuery, session: AsyncSession, user):
    orders = OrdersDAO(session)
    await orders.clear_cart(user.id)
    await session.commit()

    await render_catalog(cb, session)
