from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.dao.order_filters import OrderFilterDAO
from bot_refactored.services.order_list_renderer import render_orders
from bot_refactored.keyboards.order_filters import order_filter_kb
from bot_refactored.constants.roles import ADMINS
from bot_refactored.models.order import OrderStatus

router = Router(name="admin_orders")

def _is_admin(uid: int) -> bool:
    return uid in ADMINS


@router.callback_query(F.data == "admin:orders")
async def admin_orders(cb: CallbackQuery):
    if not _is_admin(cb.from_user.id):
        return
    await cb.message.edit_text(
        "🔍 Фильтр заказов:",
        reply_markup=order_filter_kb("admin:orders")
    )


@router.callback_query(F.data.startswith("admin:orders:status:"))
async def admin_orders_status(cb: CallbackQuery, session: AsyncSession):
    if not _is_admin(cb.from_user.id):
        return

    status = OrderStatus(cb.data.split(":")[-1])
    orders = await OrderFilterDAO.filter_orders(
        session,
        status=status,
    )

    await cb.message.edit_text(render_orders(orders))

