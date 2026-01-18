from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.models.order import Order
from bot.constants.order_status import OrderStatus
from bot.constants.callbacks import CB
from bot.keyboards.inline.operator_orders import operator_orders_kb
from bot.keyboards.inline.operator_confirm import confirm_reject_kb

PAGE_SIZE = 1

router = Router(name="operator_orders_paginated")

@router.callback_query(F.data == CB.OP_ORDERS)
async def orders_first_page(cb: CallbackQuery, *, session: AsyncSession | None = None):
    await show_page(cb, session, page=0)

@router.callback_query(F.data.startswith(CB.OP_ORDERS_PAGE))
async def orders_page(cb: CallbackQuery, *, session: AsyncSession | None = None):
    page = int(cb.data.split(":")[-1])
    await show_page(cb, session, page)

async def show_page(cb, session: AsyncSession | None = None, page: int):
    offset = page * PAGE_SIZE
    result = await session.execute(
        select(Order)
        .where(Order.status == OrderStatus.PAID_PENDING)
        .offset(offset)
        .limit(PAGE_SIZE + 1)
    )
    orders = result.scalars().all()

    if not orders:
        await cb.message.edit_text(
            "рџ“­ Р—Р°РєР°Р·РѕРІ РЅРµС‚",
            reply_markup=operator_orders_kb(page, False, False),
        )
        await cb.answer()
        return

    current = orders[0]
    has_next = len(orders) > PAGE_SIZE
    has_prev = page > 0

    await cb.message.edit_text(
        f"рџ“¦ <b>Р—Р°РєР°Р· #{current.id}</b>\n"
        f"рџ‘¤ РљР»РёРµРЅС‚: {current.client_id}",
        reply_markup=confirm_reject_kb(current.id),
    )
    await cb.message.edit_reply_markup(
        reply_markup=operator_orders_kb(page, has_prev, has_next),
    )
    await cb.answer()


