from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.keyboards.client.cart import cart_inline_kb
from bot.routers.client.catalog import render_catalog

router = Router(name="client_cart")


# ============================
# OPEN CART
# ============================

@router.callback_query(F.data == CB.CART_OPEN)
async def open_cart(cb: CallbackQuery, session: AsyncSession):
    await render_cart(cb, session)


async def render_cart(cb: CallbackQuery, session: AsyncSession):
    order = await OrdersDAO.get_or_create_cart(session, cb.from_user.id)

    if not order.items:
        await cb.message.edit_text(
            "🧺 <b>Корзина пуста</b>\n\nВыберите товары в каталоге.",
            reply_markup=None,
        )
        return

    total = sum(item.qty * item.price for item in order.items)

    text = ["🧺 <b>Корзина</b>\n"]
    for item in order.items:
        text.append(
            f"• {item.product.title} × {item.qty} = {item.qty * item.price} ₽"
        )

    text.append(f"\n<b>Итого:</b> {total} ₽")

    await cb.message.edit_text(
        "\n".join(text),
        reply_markup=cart_inline_kb(order.items),
    )


# ============================
# REMOVE ITEM
# ============================

@router.callback_query(F.data.startswith("item:remove:"))
async def remove_item(cb: CallbackQuery, session: AsyncSession):
    item_id = int(cb.data.split(":")[2])

    await OrdersDAO.remove_item(
        session=session,
        client_id=cb.from_user.id,
        item_id=item_id,
    )
    await session.commit()

    await render_cart(cb, session)


# ============================
# CLEAR CART
# ============================

@router.callback_query(F.data == CB.CART_CLEAR)
async def clear_cart(cb: CallbackQuery, session: AsyncSession):
    await OrdersDAO.clear_cart(session, cb.from_user.id)
    await session.commit()

    await render_catalog(cb, session)

