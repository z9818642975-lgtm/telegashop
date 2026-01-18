from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.dao.order_filters import OrderFilterDAO
from bot_refactored.services.order_list_renderer import render_orders
from bot_refactored.keyboards.order_filters import order_filter_kb
from bot_refactored.models.order import OrderStatus

router = Router(name="operator_orders_filter")


@router.callback_query(F.data == "operator:orders")
async def operator_orders(cb: CallbackQuery):
    await cb.message.edit_text(
        "🔍 Мои заказы:",
        reply_markup=order_filter_kb("operator:orders")
    )


@router.callback_query(F.data.startswith("operator:orders:status:"))
async def operator_orders_status(cb: CallbackQuery, session: AsyncSession):
    status = OrderStatus(cb.data.split(":")[-1])

    orders = await OrderFilterDAO.filter_orders(
        session,
        status=status,
        operator_id=cb.from_user.id,  # 🔒 защита
    )

    await cb.message.edit_text(render_orders(orders))

