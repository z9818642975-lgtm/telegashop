from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.constants.callbacks import CB
from bot.keyboards.inline.operator_panel import operator_panel_kb
from bot.keyboards.inline.operator_confirm import confirm_reject_kb
from bot.models.order import Order
from bot.constants.order_status import OrderStatus

router = Router(name="operator_panel")

@router.callback_query(F.data == CB.OPERATOR_PANEL)
async def operator_panel(cb: CallbackQuery):
    await cb.message.edit_text(
        "рџ‘· <b>РџР°РЅРµР»СЊ РѕРїРµСЂР°С‚РѕСЂР°</b>",
        reply_markup=operator_panel_kb(),
    )
    await cb.answer()

@router.callback_query(F.data == CB.OPERATOR_ORDERS)
async def operator_orders(cb: CallbackQuery, *, session: AsyncSession | None = None):
    result = await session.execute(
        select(Order).where(Order.status == OrderStatus.PAID_PENDING)
    )
    orders = result.scalars().all()

    if not orders:
        await cb.message.edit_text(
            "рџ“­ РќРµС‚ Р·Р°РєР°Р·РѕРІ",
            reply_markup=operator_panel_kb(),
        )
        await cb.answer()
        return

    order = orders[0]  # MVP: РїРµСЂРІС‹Р№ Р·Р°РєР°Р·
    await cb.message.edit_text(
        f"рџ“¦ <b>Р—Р°РєР°Р· #{order.id}</b>\nРџРѕР»СЊР·РѕРІР°С‚РµР»СЊ: {order.client_id}",
        reply_markup=confirm_reject_kb(order.id),
    )
    await cb.answer()


