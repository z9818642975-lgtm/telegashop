from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.fsm.checkout_fsm import CheckoutFSM

from bot.keyboards.client.delivery import delivery_kb

router = Router(name="client_checkout")


# ============================
# START CHECKOUT
# ============================

@router.callback_query(F.data == CB.CART_CHECKOUT)
async def start_checkout(cb: CallbackQuery, session: AsyncSession, state):
    order = await OrdersDAO.get_or_create_cart(session, cb.from_user.id)
    if not order.items:
        await cb.answer("Корзина пуста", show_alert=True)
        return

    await state.set_state(CheckoutFSM.delivery)

    await cb.message.edit_text(
        "🚚 <b>Выберите способ доставки</b>",
        reply_markup=delivery_kb(),
    )


# ============================
# DELIVERY TYPE
# ============================

@router.callback_query(
    CheckoutFSM.delivery,
    F.data.in_({CB.DELIVERY_PICKUP, CB.DELIVERY_COURIER}),
)
async def select_delivery(cb: CallbackQuery, session: AsyncSession, state):
    delivery_type = cb.data.split(":")[1]

    await OrdersDAO.set_delivery_type(
        session=session,
        client_id=cb.from_user.id,
        delivery_type=delivery_type,
    )
    await session.commit()

    if delivery_type == "pickup":
        shift = await OperatorShiftDAO.get_active_shift(session)
        address = shift.pickup_address if shift else "уточняется"

        await state.set_state(CheckoutFSM.payment)

        await cb.message.edit_text(
            f"📍 <b>Самовывоз</b>\n\nАдрес: {address}\n\nПерейдите к оплате.",
            reply_markup=None,
        )
    else:
        await state.set_state(CheckoutFSM.address)

        await cb.message.edit_text(
            "📦 <b>Введите адрес доставки</b>",
            reply_markup=None,
        )

