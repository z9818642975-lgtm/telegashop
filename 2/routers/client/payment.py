from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.fsm.checkout_fsm import CheckoutFSM

from bot.keyboards.client.payment import payment_kb
from bot.models.enums import OrderStatus

router = Router(name="client_payment")


# ============================
# OPEN PAYMENT
# ============================

@router.callback_query(
    CheckoutFSM.payment,
    F.data.in_({CB.PAYMENT_CASH, CB.PAYMENT_CARD}),
)
async def select_payment(cb: CallbackQuery, session: AsyncSession, state):
    method = cb.data.split(":")[1]

    await OrdersDAO.set_payment_method(
        session=session,
        client_id=cb.from_user.id,
        method=method,
    )
    await OrdersDAO.set_status(
        session=session,
        client_id=cb.from_user.id,
        status=OrderStatus.AWAITING_PAYMENT,
    )
    await session.commit()

    await state.clear()

    await cb.message.edit_text(
        "💳 <b>Оплата</b>\n\n"
        "Переведите средства и загрузите чек.\n"
        "После проверки оператором заказ будет принят.",
        reply_markup=payment_kb(),
    )

