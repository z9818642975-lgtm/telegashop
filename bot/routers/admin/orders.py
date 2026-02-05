# bot/routers/admin/orders.py
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import AdminOrderForce, AdminOrders, BackToAdminOrders
from bot.dao.order_items_dao import OrderItemsDAO
from bot.dao.orders_dao import OrdersDAO
from bot.dao.users_dao import UsersDAO
from bot.dao.warehouses_dao import WarehousesDAO
from bot.filters.role import RoleFilter
from bot.models.enums import OrderStatus
from bot.utils.safe_edit import safe_edit_text

PAGE_SIZE = 8
router = Router(name="admin_orders")


# ============================================================
# 📋 LIST / CARD / ITEMS
# ============================================================

@router.callback_query(RoleFilter("admin"), AdminOrders.filter())
async def admin_orders_entry(
    cb: CallbackQuery,
    callback_data: AdminOrders,
    session: AsyncSession,
):
    # ---------- CARD / ITEMS ----------
    if callback_data.order_id is not None:
        if callback_data.view == "items":
            await _order_items(cb, callback_data, session)
        else:
            await _order_card(cb, callback_data, session)
        return

    # ---------- LIST ----------
    page = callback_data.page
    status = callback_data.status

    dao = OrdersDAO(session)
    orders, total = await dao.list_page(
        page=page,
        limit=PAGE_SIZE,
        status=status,
    )

    rows: list[list[InlineKeyboardButton]] = []

    for o in orders:
        rows.append([
            InlineKeyboardButton(
                text=f"#{o.id} · {o.status}",
                callback_data=AdminOrders(order_id=o.id).pack(),
            )
        ])

    # ---------- PAGINATION ----------
    nav = []

    if page > 1:
        nav.append(
            InlineKeyboardButton(
                text="А ⬅ Назад",
                callback_data=AdminOrders(
                    page=page - 1,
                    status=status,
                ).pack(),
            )
        )

    if page * PAGE_SIZE < total:
        nav.append(
            InlineKeyboardButton(
                text="А Вперёд ➡",
                callback_data=AdminOrders(
                    page=page + 1,
                    status=status,
                ).pack(),
            )
        )

    if nav:
        rows.append(nav)

    # ---------- FILTERS ----------
    rows.append([
        InlineKeyboardButton(
            text="А 💰 Оплаченные",
            callback_data=AdminOrders(
                page=1,
                status=OrderStatus.PAID,
            ).pack(),
        ),
        InlineKeyboardButton(
            text="А 🛠 В работе",
            callback_data=AdminOrders(
                page=1,
                status=OrderStatus.IN_WORK,
            ).pack(),
        ),
    ])

    rows.append([
        InlineKeyboardButton(
            text="А 📋 Все заказы",
            callback_data=AdminOrders(
                page=1,
                status=None,
            ).pack(),
        )
    ])

    rows.append([
        InlineKeyboardButton(
            text="А ⬅ В админ-меню",
            callback_data=BackToAdminOrders().pack(),
        )
    ])

    await safe_edit_text(
        cb.message,
        text="А 📋 <b>Заказы</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="HTML",
    )
    await cb.answer()


# ============================================================
# 📦 ORDER CARD
# ============================================================

async def _order_card(
    cb: CallbackQuery,
    data: AdminOrders,
    session: AsyncSession,
):
    orders = OrdersDAO(session)
    warehouses = WarehousesDAO(session)
    users = UsersDAO(session)

    order = await orders.get_by_id(data.order_id)
    if not order:
        await cb.answer("Заказ не найден", show_alert=True)
        return

    wh = await warehouses.get_by_id(order.warehouse_id) if order.warehouse_id else None
    operator = await users.get_by_id(order.operator_id) if order.operator_id else None

    text = (
        f"📦 <b>Заказ #{order.id}</b>\n\n"
        f"Статус: <b>{order.status}</b>\n"
        f"Сумма: {order.total_price} ₽\n"
    )

    if wh:
        text += f"🏬 Склад: {wh.title}\n"
    if operator:
        text += f"👷 Оператор: {operator.id}\n"

    text += f"\nСоздан: {order.created_at:%d.%m.%Y %H:%M}\n"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А 📦 Позиции",
                    callback_data=AdminOrders(
                        order_id=order.id,
                        view="items",
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="А ❌ Закрыть принудительно",
                    callback_data=AdminOrderForce(order_id=order.id).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="А ⬅ Назад",
                    callback_data=AdminOrders(
                        page=1,
                        status=data.status,
                    ).pack(),
                ),
            ],
        ]
    )

    await safe_edit_text(
        cb.message,
        text=text,
        reply_markup=kb,
        parse_mode="HTML",
    )
    await cb.answer()


# ============================================================
# 📦 ORDER ITEMS
# ============================================================

async def _order_items(
    cb: CallbackQuery,
    data: AdminOrders,
    session: AsyncSession,
):
    rows = await OrderItemsDAO(session).list_by_order(data.order_id)

    if not rows:
        await cb.answer("Позиции отсутствуют", show_alert=True)
        return

    text = "📦 <b>Позиции заказа</b>\n\n"

    for r in rows:
        text += (
            f"{r.product.title}\n"
            f"{r.qty} × {r.price} ₽ = {r.qty * r.price} ₽\n\n"
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="А ⬅ К заказу",
                    callback_data=AdminOrders(
                        order_id=data.order_id,
                    ).pack(),
                ),
            ]
        ]
    )

    await safe_edit_text(
        cb.message,
        text=text,
        reply_markup=kb,
        parse_mode="HTML",
    )
    await cb.answer()


# ============================================================
# 🛑 FORCE CLOSE
# ============================================================

@router.callback_query(RoleFilter("admin"), AdminOrderForce.filter())
async def admin_order_force_close(
    cb: CallbackQuery,
    callback_data: AdminOrderForce,
    session: AsyncSession,
):
    await OrdersDAO(session).force_status(
        order_id=callback_data.order_id,
        status=OrderStatus.DONE,
    )
    await session.commit()

    await cb.answer("Заказ закрыт", show_alert=True)

    await _order_card(
        cb,
        AdminOrders(order_id=callback_data.order_id),
        session,
    )