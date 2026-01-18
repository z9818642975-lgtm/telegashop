$base = "bot_refactored"

function MkFile($path, $content) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
    Set-Content -Path $path -Value $content -Encoding UTF8
}

# ======================================================
# 1. DAO: ФИЛЬТРАЦИЯ ЗАКАЗОВ
# ======================================================
MkFile "$base/dao/order_filters.py" @'
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.models.order import Order, OrderStatus


class OrderFilterDAO:

    @staticmethod
    async def filter_orders(
        session: AsyncSession,
        *,
        status: OrderStatus | None = None,
        operator_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Order]:

        stmt = select(Order)

        if status:
            stmt = stmt.where(Order.status == status)

        if operator_id:
            stmt = stmt.where(Order.operator_id == operator_id)

        if date_from:
            stmt = stmt.where(Order.created_at >= date_from)

        if date_to:
            stmt = stmt.where(Order.created_at <= date_to)

        res = await session.execute(stmt.order_by(Order.created_at.desc()))
        return res.scalars().all()
'@

# ======================================================
# 2. SERVICE: РЕНДЕР СПИСКА ЗАКАЗОВ
# ======================================================
MkFile "$base/services/order_list_renderer.py" @'
from bot_refactored.models.order import Order


def render_orders(orders: list[Order]) -> str:
    if not orders:
        return "❌ Заказы не найдены"

    lines = ["📦 Заказы:"]
    for o in orders:
        lines.append(
            f"#{o.id} | {o.status} | "
            f"оператор: {o.operator_id or '-'} | "
            f"{o.created_at:%Y-%m-%d %H:%M}"
        )
    return "\n".join(lines)
'@

# ======================================================
# 3. INLINE-КНОПКИ ФИЛЬТРОВ
# ======================================================
MkFile "$base/keyboards/order_filters.py" @'
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_refactored.models.order import OrderStatus


def order_filter_kb(prefix: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("🆕 NEW", callback_data=f"{prefix}:status:{OrderStatus.NEW}"),
            InlineKeyboardButton("✅ ACCEPTED", callback_data=f"{prefix}:status:{OrderStatus.ACCEPTED}"),
        ],
        [
            InlineKeyboardButton("⏳ WAIT", callback_data=f"{prefix}:status:{OrderStatus.WAITING_CONFIRMATION}"),
            InlineKeyboardButton("💰 PAID", callback_data=f"{prefix}:status:{OrderStatus.PAID}"),
        ],
        [
            InlineKeyboardButton("✔ DONE", callback_data=f"{prefix}:status:{OrderStatus.DONE}"),
        ],
    ])
'@

# ======================================================
# 4. АДМИН: ПРОСМОТР С ФИЛЬТРАМИ
# ======================================================
MkFile "$base/routers/admin/orders.py" @'
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
'@

# ======================================================
# 5. ОПЕРАТОР: ПРОСМОТР С ФИЛЬТРАМИ
# ======================================================
MkFile "$base/routers/operator/orders.py" @'
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
'@

Write-Host "Order filters (admin + operator) added." -ForegroundColor Green
