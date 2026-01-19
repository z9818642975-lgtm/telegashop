from __future__ import annotations

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.constants.callbacks import CB

from bot.dao.users_dao import UsersDAO
from bot.dao.products_dao import ProductsDAO
from bot.dao.warehouses_dao import WarehousesDAO
from bot.dao.orders_dao import OrdersDAO
from bot.dao.payment_dao import PaymentDAO
from bot.dao.statistics_dao import StatisticsDAO

from bot.models.enums import OrderStatus

from bot.keyboards.admin.panel import admin_panel_kb
from bot.keyboards.admin.products import products_kb
from bot.keyboards.admin.warehouses import warehouses_kb
from bot.keyboards.admin.operators import operators_kb
from bot.keyboards.admin.payments import banks_kb
from bot.keyboards.admin.orders import admin_orders_kb

router = Router(name="admin")

# ============================================================
# ENTRY
# ============================================================

@router.message(RoleFilter("admin"), F.text == "👑 Админ")
async def admin_panel(message: Message):
    await message.answer(
        "👑 Админ-панель",
        reply_markup=admin_panel_kb(),
    )

# ============================================================
# PRODUCTS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:products"))
async def admin_products(call: CallbackQuery, session: AsyncSession):
    dao = ProductsDAO(session)
    products = await dao.list_all()
    

    await call.message.edit_text(
        "📦 Товары",
        reply_markup=products_kb(products),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:product:toggle"))
async def admin_product_toggle(call: CallbackQuery, session: AsyncSession):
    product_id = int(call.data.split(":")[-1])
    await dao.toggle_active(product_id)    await session.commit()
    await call.answer("OK")

# ============================================================
# WAREHOUSES
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:warehouses"))
async def admin_warehouses(call: CallbackQuery, session: AsyncSession):
    dao = WarehousesDAO(session)
    warehouses = await dao.list_all()
    await call.message.edit_text(
        "🏬 Склады",
        reply_markup=warehouses_kb(warehouses),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:warehouse:move"))
async def admin_warehouse_move(call: CallbackQuery, session: AsyncSession):
    _, _, from_id, to_id, product_id, qty = call.data.split(":")
    dao = WarehousesDAO(session)
    await dao.move(
        from_warehouse_id=int(from_id),
        to_warehouse_id=int(to_id),
        product_id=int(product_id),
        quantity=int(qty),
    )
    await session.commit()
    await call.answer("Перемещено")

# ============================================================
# OPERATORS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:operators"))
async def admin_operators(call: CallbackQuery, session: AsyncSession):
    users = UsersDAO(session)
    operators = await users.list_operators()
    await call.message.edit_text(
        "👷 Операторы",
        reply_markup=operators_kb(operators),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:operator:toggle"))
async def admin_operator_toggle(call: CallbackQuery, session: AsyncSession):
    operator_id = int(call.data.split(":")[-1])
    users = UsersDAO(session)
    await users.toggle_active(operator_id)
    await session.commit()
    await call.answer("OK")

# ============================================================
# BANKS / PAYMENTS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == "admin:banks")
async def admin_banks(call: CallbackQuery, session: AsyncSession):
    dao = PaymentDAO(session)
    banks = await dao.list_requisites()
    await call.message.edit_text(
        "💳 Реквизиты",
        reply_markup=banks_kb(banks),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:bank:toggle"))
async def admin_bank_toggle(call: CallbackQuery, session: AsyncSession):
    bank_id = int(call.data.split(":")[-1])
    dao = PaymentDAO(session)
    await dao.toggle_bank(bank_id)
    await session.commit()
    await call.answer("OK")

# ============================================================
# ORDERS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == "admin:orders")
async def admin_orders(call: CallbackQuery, session: AsyncSession):
    dao = OrdersDAO(session)
    orders = await dao.list_recent(limit=20)
    await call.message.edit_text(
        "📋 Заказы",
        reply_markup=admin_orders_kb(orders),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:order:force"))
async def admin_force_order(call: CallbackQuery, session: AsyncSession):
    _, _, order_id, status = call.data.split(":")
    dao = OrdersDAO(session)
    await dao.force_status(
        order_id=int(order_id),
        status=OrderStatus(status),
    )
    await session.commit()
    await call.answer("Статус изменён")

# ============================================================
# PAYMENTS ACTIONS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:payment:approve"))
async def admin_payment_approve(call: CallbackQuery, session: AsyncSession):
    payment_id = int(call.data.split(":")[-1])
    payments = PaymentDAO(session)
    orders = OrdersDAO(session)

    payment = await payments.get(payment_id)
    await payments.approve(payment_id)
    await orders.mark_paid(payment.order_id)

    await session.commit()
    await call.answer("Платёж подтверждён")

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:payment:reject"))
async def admin_payment_reject(call: CallbackQuery, session: AsyncSession):
    payment_id = int(call.data.split(":")[-1])
    payments = PaymentDAO(session)
    await payments.reject(payment_id, reason="Отклонено администратором")
    await session.commit()
    await call.answer("Отклонено")

# ============================================================
# STATISTICS
# ============================================================

@router.callback_query(F.data == "admin:stats:week")
async def stats_week(call: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    data = await dao.period_summary(days=7)
    await call.message.edit_text(
        "📊 <b>Неделя</b>\n\n"
        f"📦 Заказов: {data['orders_total']}\n"
        f"✅ Оплачено: {data['orders_paid']}\n"
        f"💰 Оборот: {data['revenue']} ₽\n"
        f"🧾 Средний чек: {data['avg_check']} ₽",
        parse_mode="HTML",
    )
    await call.answer()

@router.callback_query(F.data == "admin:stats:month")
async def stats_month(call: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    data = await dao.period_summary(days=30)
    await call.message.edit_text(
        "📊 <b>Месяц</b>\n\n"
        f"📦 Заказов: {data['orders_total']}\n"
        f"✅ Оплачено: {data['orders_paid']}\n"
        f"💰 Оборот: {data['revenue']} ₽\n"
        f"🧾 Средний чек: {data['avg_check']} ₽",
        parse_mode="HTML",
    )
    await call.answer()

@router.callback_query(F.data == "admin:stats:per_operator")
async def stats_per_operator(call: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    rows = await dao.per_operator(days=30)

    text = "👤 <b>Операторы (30 дней)</b>\n\n"
    for r in rows:
        text += f"{r['name']}\n  📦 {r['orders']} | 💰 {r['revenue']} ₽\n"

    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "admin:stats:per_warehouse")
async def stats_per_warehouse(call: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    rows = await dao.per_warehouse(days=30)

    text = "🏬 <b>Склады (30 дней)</b>\n\n"
    for r in rows:
        text += f"{r['title']}\n  📦 {r['orders']} | 💰 {r['revenue']} ₽\n"

    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "admin:stats:graph")
async def stats_graph(call: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    data = await dao.revenue_timeseries(days=30)

    text = "📈 <b>Выручка по дням (30 дней)</b>\n\n"
    for d in data:
        text += f"{d['date']} → {d['revenue']} ₽\n"

    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()


