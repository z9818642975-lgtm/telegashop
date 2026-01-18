from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.keyboards.client.cart import cart_inline_kb
from bot.models.user import User
from bot.services.catalog_service import show_catalog

router = Router(name="client_cart")


# ============================
# OPEN CART
# ============================

@router.callback_query(F.data == CB.CART_OPEN)
async def open_cart(
    cb: CallbackQuery,
    *,
    session: AsyncSession,
    user: User,
):
    await render_cart(cb, session, user)


async def render_cart(
    cb: CallbackQuery,
    session: AsyncSession,
    user: User,
):
    order = await OrdersDAO.get_or_create_cart(session, user.id)

    if not order.items:
        await cb.message.edit_text(
            "рџ§є <b>РљРѕСЂР·РёРЅР° РїСѓСЃС‚Р°</b>\n\n"
            "Р’С‹Р±РµСЂРёС‚Рµ С‚РѕРІР°СЂС‹ РІ РєР°С‚Р°Р»РѕРіРµ.",
        )
        return

    total = sum(item.qty * item.price for item in order.items)

    lines = ["рџ§є <b>РљРѕСЂР·РёРЅР°</b>\n"]
    for item in order.items:
        lines.append(
            f"вЂў {item.product.title} Г— {item.qty} = {item.qty * item.price} в‚Ѕ"
        )

    lines.append(f"\n<b>РС‚РѕРіРѕ:</b> {total} в‚Ѕ")

    await cb.message.edit_text(
        "\n".join(lines),
        reply_markup=cart_inline_kb(order.items),
    )


# ============================
# REMOVE ITEM
# ============================

@router.callback_query(F.data.startswith("client:item:remove:"))
async def remove_item(
    cb: CallbackQuery,
    *,
    session: AsyncSession,
    user: User,
):
    item_id = int(cb.data.split(":")[2])

    await OrdersDAO.remove_item(
        session=session,
        client_id=user.id,
        item_id=item_id,
    )

    await render_cart(cb, session, user)


# ============================
# CLEAR CART
# ============================

@router.callback_query(F.data == CB.CART_CLEAR)
async def clear_cart(
    cb: CallbackQuery,
    *,
    session: AsyncSession,
    user: User,
):
    await OrdersDAO.clear_cart(session, user.id)

    await show_catalog(
        message=cb.message,
        session=session,
        user=user,
    )

