from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.orders_dao import OrdersDAO
from bot.models.user import User
from bot.services.catalog_service import show_catalog

router = Router(name="client_quantity")


@router.callback_query(F.data.startswith("client:qty:"))
async def select_quantity(
    cb: CallbackQuery,
    *,
    session: AsyncSession,
    user: User,
):
    """
    qty:{product_id}:{qty}
    """
    try:
        _, product_id, qty = cb.data.split(":")
        product_id = int(product_id)
        qty = int(qty)
    except ValueError:
        await cb.answer("РћС€РёР±РєР° РІС‹Р±РѕСЂР° РєРѕР»РёС‡РµСЃС‚РІР°", show_alert=True)
        return

    if qty <= 0:
        await cb.answer("РќРµРєРѕСЂСЂРµРєС‚РЅРѕРµ РєРѕР»РёС‡РµСЃС‚РІРѕ", show_alert=True)
        return

    await OrdersDAO.add_item(
        session=session,
        client_id=user.id,
        product_id=product_id,
        qty=qty,
    )

    await cb.answer("Р”РѕР±Р°РІР»РµРЅРѕ РІ РєРѕСЂР·РёРЅСѓ")

    # РљРђРќРћРќ: РІРѕР·РІСЂР°С‚ РІ РєР°С‚Р°Р»РѕРі, Р±РµР· РЅРѕРІС‹С… СЃРѕРѕР±С‰РµРЅРёР№
    await show_catalog(
        message=cb.message,
        session=session,
        user=user,
    )

