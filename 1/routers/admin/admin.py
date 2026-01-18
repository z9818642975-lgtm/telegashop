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

# РІСњРЉ DISABLED (admin/operator text handler)
async def admin_panel(message: Message):
    await message.answer(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В Р вЂ Р В РІР‚С™Р вЂ™Р’В Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІвЂћСћР В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р Р‹Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦-Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р В Р вЂ№Р В Р’В Р В РІР‚В°",
        reply_markup=admin_panel_kb(),
    )

# ============================================================
# PRODUCTS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == CB.ADMIN_PRODUCTS)
async def admin_products(call: CallbackQuery, session: AsyncSession | None = None):
    products = await ProductsDAO.list_all(session)

    await call.message.edit_text(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В РІР‚в„ўР вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р Р‹Р РЋРІР‚С”Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ",
        reply_markup=products_kb(products),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:product:toggle"))
async def admin_product_toggle(call: CallbackQuery, session: AsyncSession | None = None):
    product_id = int(call.data.split(":")[-1])
    await ProductsDAO.toggle_active(session, product_id)
    await session.commit()
    await call.answer("OK")

# ============================================================
# WAREHOUSES
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == CB.ADMIN_WAREHOUSES)
async def admin_warehouses(call: CallbackQuery, session: AsyncSession | None = None):
    dao = WarehousesDAO(session)
    warehouses = await dao.list_all()
    await call.message.edit_text(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р’В Р В Р РЏР В РІР‚в„ўР вЂ™Р’В¬ Р В Р’В Р вЂ™Р’В Р В Р’В Р В РІР‚в„–Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ",
        reply_markup=warehouses_kb(warehouses),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:warehouse:move"))
async def admin_warehouse_move(call: CallbackQuery, session: AsyncSession | None = None):
    _, _, from_id, to_id, product_id, qty = call.data.split(":")
    dao = WarehousesDAO(session)
    await dao.move(
        from_warehouse_id=int(from_id),
        to_warehouse_id=int(to_id),
        product_id=int(product_id),
        quantity=int(qty),
    )
    await session.commit()
    await call.answer("Р В Р’В Р вЂ™Р’В Р В Р Р‹Р РЋРЎСџР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р Р‹Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›")

# ============================================================
# OPERATORS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == CB.ADMIN_OPERATORS)
async def admin_operators(call: CallbackQuery, session: AsyncSession | None = None):
    users = UsersDAO(session)
    operators = await users.list_operators()
    await call.message.edit_text(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В РІР‚в„ўР вЂ™Р’В· Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ",
        reply_markup=operators_kb(operators),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:operator:toggle"))
async def admin_operator_toggle(call: CallbackQuery, session: AsyncSession | None = None):
    operator_id = int(call.data.split(":")[-1])
    users = UsersDAO(session)
    await users.toggle_active(operator_id)
    await session.commit()
    await call.answer("OK")

# ============================================================
# BANKS / PAYMENTS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == "admin:banks")
async def admin_banks(call: CallbackQuery, session: AsyncSession | None = None):
    dao = PaymentDAO(session)
    banks = await dao.list_requisites()
    await call.message.edit_text(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РЎС›Р В Р Р‹Р Р†Р вЂљРІР‚Сљ Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В·Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ",
        reply_markup=banks_kb(banks),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:bank:toggle"))
async def admin_bank_toggle(call: CallbackQuery, session: AsyncSession | None = None):
    bank_id = int(call.data.split(":")[-1])
    dao = PaymentDAO(session)
    await dao.toggle_bank(bank_id)
    await session.commit()
    await call.answer("OK")

# ============================================================
# ORDERS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == "admin:orders")
async def admin_orders(call: CallbackQuery, session: AsyncSession | None = None):
    dao = OrdersDAO(session)
    orders = await dao.list_recent(limit=20)
    await call.message.edit_text(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В·Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ",
        reply_markup=admin_orders_kb(orders),
    )
    await call.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:order:force"))
async def admin_force_order(call: CallbackQuery, session: AsyncSession | None = None):
    _, _, order_id, status = call.data.split(":")
    dao = OrdersDAO(session)
    await dao.force_status(
        order_id=int(order_id),
        status=OrderStatus(status),
    )
    await session.commit()
    await call.answer("Р В Р’В Р вЂ™Р’В Р В Р’В Р В РІР‚в„–Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р В Р вЂ№Р В Р Р‹Р Р†Р вЂљРЎС™Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚Сљ Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В·Р В Р’В Р вЂ™Р’В Р В Р Р‹Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦")

# ============================================================
# PAYMENTS ACTIONS
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:payment:approve"))
async def admin_payment_approve(call: CallbackQuery, session: AsyncSession | None = None):
    payment_id = int(call.data.split(":")[-1])
    payments = PaymentDAO(session)
    orders = OrdersDAO(session)

    payment = await payments.get(payment_id)
    await payments.approve(payment_id)
    await orders.mark_paid(payment.order_id)

    await session.commit()
    await call.answer("Р В Р’В Р вЂ™Р’В Р В Р Р‹Р РЋРЎСџР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В¶ Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В¶Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦")

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:payment:reject"))
async def admin_payment_reject(call: CallbackQuery, session: AsyncSession | None = None):
    payment_id = int(call.data.split(":")[-1])
    payments = PaymentDAO(session)
    await payments.reject(payment_id, reason="Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС› Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р Р‹Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚СљР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р Р‹Р вЂ™Р’В")
    await session.commit()
    await call.answer("Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›")

# ============================================================
# STATISTICS
# ============================================================

@router.callback_query(F.data == "admin:stats:week")
async def stats_week(call: CallbackQuery, session: AsyncSession | None = None):
    dao = StatisticsDAO(session)
    data = await dao.period_summary(days=7)
    await call.message.edit_text(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В Р’В Р Р†Р вЂљР’В° <b>Р В Р’В Р вЂ™Р’В Р В Р Р‹Р РЋРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р В Р вЂ№Р В Р’В Р В Р РЏ</b>\n\n"
        f"Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В РІР‚в„ўР вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В·Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В : {data['orders_total']}\n"
        f"Р В Р’В Р В РІР‚В Р В Р Р‹Р РЋРІвЂћСћР В Р вЂ Р В РІР‚С™Р вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р В Р вЂ№Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›: {data['orders_paid']}\n"
        f"Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РЎС›Р В РІР‚в„ўР вЂ™Р’В° Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В±Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћ: {data['revenue']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљР’В¦\n"
        f"Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В РІР‚в„ўР вЂ™Р’В§Р В Р Р‹Р Р†Р вЂљРЎС› Р В Р’В Р вЂ™Р’В Р В Р’В Р В РІР‚в„–Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р вЂ Р Р†Р вЂљРЎвЂєР Р†Р вЂљРІР‚Сљ Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р В Р вЂ№Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљ: {data['avg_check']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљР’В¦",
        parse_mode="HTML",
    )
    await call.answer()

@router.callback_query(F.data == "admin:stats:month")
async def stats_month(call: CallbackQuery, session: AsyncSession | None = None):
    dao = StatisticsDAO(session)
    data = await dao.period_summary(days=30)
    await call.message.edit_text(
        "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В Р’В Р Р†Р вЂљР’В° <b>Р В Р’В Р вЂ™Р’В Р В Р Р‹Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚СљР В Р’В Р В Р вЂ№Р В Р’В Р В Р РЏР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р вЂ™Р’В </b>\n\n"
        f"Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В РІР‚в„ўР вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В·Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В : {data['orders_total']}\n"
        f"Р В Р’В Р В РІР‚В Р В Р Р‹Р РЋРІвЂћСћР В Р вЂ Р В РІР‚С™Р вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р В Р вЂ№Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›: {data['orders_paid']}\n"
        f"Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РЎС›Р В РІР‚в„ўР вЂ™Р’В° Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В±Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћ: {data['revenue']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљР’В¦\n"
        f"Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В РІР‚в„ўР вЂ™Р’В§Р В Р Р‹Р Р†Р вЂљРЎС› Р В Р’В Р вЂ™Р’В Р В Р’В Р В РІР‚в„–Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р вЂ Р Р†Р вЂљРЎвЂєР Р†Р вЂљРІР‚Сљ Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р В Р вЂ№Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљ: {data['avg_check']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљР’В¦",
        parse_mode="HTML",
    )
    await call.answer()

@router.callback_query(F.data == "admin:stats:per_operator")
async def stats_per_operator(call: CallbackQuery, session: AsyncSession | None = None):
    dao = StatisticsDAO(session)
    rows = await dao.per_operator(days=30)

    text = "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В РІР‚в„ўР вЂ™Р’В¤ <b>Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎвЂќР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ (30 Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р вЂ Р Р†Р вЂљРЎвЂєР Р†Р вЂљРІР‚Сљ)</b>\n\n"
    for r in rows:
        text += f"{r['name']}\n  Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В РІР‚в„ўР вЂ™Р’В¦ {r['orders']} | Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РЎС›Р В РІР‚в„ўР вЂ™Р’В° {r['revenue']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљР’В¦\n"

    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "admin:stats:per_warehouse")
async def stats_per_warehouse(call: CallbackQuery, session: AsyncSession | None = None):
    dao = StatisticsDAO(session)
    rows = await dao.per_warehouse(days=30)

    text = "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р’В Р В Р РЏР В РІР‚в„ўР вЂ™Р’В¬ <b>Р В Р’В Р вЂ™Р’В Р В Р’В Р В РІР‚в„–Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњ (30 Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р вЂ Р Р†Р вЂљРЎвЂєР Р†Р вЂљРІР‚Сљ)</b>\n\n"
    for r in rows:
        text += f"{r['title']}\n  Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В РІР‚в„ўР вЂ™Р’В¦ {r['orders']} | Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РЎС›Р В РІР‚в„ўР вЂ™Р’В° {r['revenue']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљР’В¦\n"

    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "admin:stats:graph")
async def stats_graph(call: CallbackQuery, session: AsyncSession | None = None):
    dao = StatisticsDAO(session)
    data = await dao.revenue_timeseries(days=30)

    text = "Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В Р вЂ Р Р†Р вЂљРЎв„ўР вЂ™Р’В¬ <b>Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РЎС›Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РІР‚вЂњР В Р’В Р В Р вЂ№Р В Р’В Р Р†Р вЂљРЎв„ўР В Р’В Р В Р вЂ№Р В Р Р‹Р Р†Р вЂљРЎС™Р В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р В Р вЂ№Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В° Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС› Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р В Р вЂ№Р В Р’В Р В Р РЏР В Р’В Р вЂ™Р’В Р В Р Р‹Р вЂ™Р’В (30 Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р вЂ Р Р†Р вЂљРЎвЂєР Р†Р вЂљРІР‚Сљ)</b>\n\n"
    for d in data:
        text += f"{d['date']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р Р†РІР‚С›РЎС› {d['revenue']} Р В Р’В Р В РІР‚В Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљР’В¦\n"

    await call.message.edit_text(text, parse_mode="HTML")
    await call.answer()


