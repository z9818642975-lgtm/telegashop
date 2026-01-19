from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.dao.payment_dao import PaymentDAO
from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.keyboards.operator.orders import sent_kb
from bot.services.order_workflow import schedule_assembling

router = Router(name="operator_orders")


# ============================
# CHECK APPROVE
# ============================

@router.callback_query(
    RoleFilter("operator"),
    F.data.startswith("operator:check:accept:")
)
async def approve_check(
    call: CallbackQuery,
    session: AsyncSession,
    user,
):
    order_id = int(call.data.split(":")[-1])

    shifts = OperatorShiftDAO(session)
    if not await shifts.is_on_shift(user.id):
        await call.answer("❌ Смена не активна", show_alert=True)
        return

    await PaymentDAO(session).approve_by_order(order_id)
    await OrdersDAO(session).mark_paid(order_id)
    await session.commit()

    await call.message.edit_text(f"✅ Чек принят\nЗаказ №{order_id}")

    # ⏱ безопасная отложенная сборка
    schedule_assembling(order_id)


# ============================
# ORDER READY
# ============================

@router.callback_query(
    RoleFilter("operator"),
    F.data.startswith("operator:order:ready:")
)
async def order_ready(
    call: CallbackQuery,
    session: AsyncSession,
    user,
):
    order_id = int(call.data.split(":")[-1])

    shifts = OperatorShiftDAO(session)
    if not await shifts.is_on_shift(user.id):
        await call.answer("❌ Смена не активна", show_alert=True)
        return

    await OrdersDAO(session).mark_ready(order_id, "Товар готов", None)
    await session.commit()

    await call.message.edit_text(
        f"📦 Заказ №{order_id} готов",
        reply_markup=sent_kb(order_id),
    )


# ============================
# ORDER SENT
# ============================

@router.callback_query(
    RoleFilter("operator"),
    F.data.startswith("operator:order:sent:")
)
async def order_sent(
    call: CallbackQuery,
    session: AsyncSession,
    user,
):
    order_id = int(call.data.split(":")[-1])

    shifts = OperatorShiftDAO(session)
    if not await shifts.is_on_shift(user.id):
        await call.answer("❌ Смена не активна", show_alert=True)
        return

    await OrdersDAO(session).mark_sent(order_id, None)
    await session.commit()

    await call.message.edit_text(
        f"🚚 Заказ №{order_id} передан курьеру"
    )

