# bot/routers/client/payment.py
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.fsm.checkout_fsm import CheckoutFSM
from bot.dao.orders_dao import OrdersDAO
from bot.models.enums import OrderStatus

router = Router(name="client_payment")


@router.callback_query(
    CheckoutFSM.payment,
    F.data.startswith("client:pay:"),
)
async def choose_payment(
    cb: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user,
):
    method = cb.data.split(":", 1)[1]

    order = await OrdersDAO(session).get_active(user.id)
    order.payment_method = method
    order.status = OrderStatus.WAITING_PAYMENT
    await session.flush()

    await state.set_state(CheckoutFSM.wait_check)

    await cb.message.edit_text("📎 Пришлите чек")


@router.message(CheckoutFSM.wait_check)
async def receive_check(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user,
):
    order = await OrdersDAO(session).get_active(user.id)
    order.status = OrderStatus.WAITING_OPERATOR
    await session.flush()

    await state.clear()

    await message.answer("⏳ Чек передан оператору")

