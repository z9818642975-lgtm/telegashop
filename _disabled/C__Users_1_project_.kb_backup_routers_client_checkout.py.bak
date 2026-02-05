# bot/routers/client/checkout.py
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


@router.callback_query(F.data == CB.CART_CHECKOUT)
async def start_checkout(
    cb: CallbackQuery,
    session: AsyncSession,
    state,
    user,
):
    orders = OrdersDAO(session)
    order = await orders.get_cart(user.id)

    if not order or not order.items:
        await cb.answer("Корзина пуста", show_alert=True)
        return

    await state.set_state(CheckoutFSM.delivery)

    await cb.message.edit_text(
        "🚚 <b>Выберите способ доставки</b>",
        reply_markup=delivery_kb(),
    )


@router.callback_query(
    CheckoutFSM.delivery,
    F.data.in_({CB.DELIVERY_PICKUP, CB.DELIVERY_COURIER}),
)
async def select_delivery(
    cb: CallbackQuery,
    session: AsyncSession,
    state,
    user,
):
    delivery_type = cb.data.split(":")[1]

    orders = OrdersDAO(session)
    order = await orders.get_cart(user.id)

    if not order:
        await cb.answer("Корзина пуста", show_alert=True)
        return

    order.delivery_type = delivery_type
    await session.commit()

    if delivery_type == "pickup":
        shift = await OperatorShiftDAO(session).get_active_shift()
        address = shift.pickup_address if shift else "уточняется"

        await state.set_state(CheckoutFSM.payment)

        await cb.message.edit_text(
            f"📍 <b>Самовывоз</b>\n\nАдрес: {address}",
        )
    else:
        await state.set_state(CheckoutFSM.address)

        await cb.message.edit_text(
            "📦 <b>Введите адрес доставки</b>",
        )
