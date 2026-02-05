# bot/routers/payment.py
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_client import PaymentMethodCB
from bot.dao.orders_dao import OrdersDAO
from bot.fsm.checkout_fsm import CheckoutFSM
from bot.models.enums import OrderStatus
from bot.utils.safe_edit import safe_edit_text

router = Router(name="client_payment")


@router.callback_query(PaymentMethodCB.filter(), CheckoutFSM.payment)
async def choose_payment(
    cb: CallbackQuery,
    callback_data: PaymentMethodCB,
    state: FSMContext,
    session: AsyncSession,
    user,
):
    order = await OrdersDAO(session).get_active(user.id)

    order.payment_method = callback_data.method
    order.status = OrderStatus.WAITING_PAYMENT
    await session.flush()

    await state.set_state(CheckoutFSM.wait_check)
    await safe_edit_text(cb.message, text="📎 Пришлите чек")


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