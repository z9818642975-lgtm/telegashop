# bot/routers/client/checkout.py
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import (
    ClientDeliveryCourier,
    ClientDeliveryPickup,
    ClientPayBank,
    ClientPaymentCancel,
    ClientPaySBP,
)
from bot.dao.orders_dao import OrdersDAO
from bot.fsm.checkout_fsm import CheckoutFSM
from bot.keyboards.client.banks import client_banks_kb

router = Router(name="client_checkout")


# === ВЫБОР ДОСТАВКИ ===

@router.callback_query(ClientDeliveryPickup.filter())
async def delivery_pickup(cb: CallbackQuery, session: AsyncSession):
    await OrdersDAO(session).set_delivery_method(
        user_id=cb.from_user.id,
        method="pickup",
    )
    await cb.message.edit_text(
        "📦 Самовывоз выбран\n\nВыберите способ оплаты:",
        reply_markup=client_banks_kb(),
    )
    await cb.answer()


@router.callback_query(ClientDeliveryCourier.filter())
async def delivery_courier(cb: CallbackQuery, state: FSMContext):
    await state.set_state(CheckoutFSM.address)
    await state.update_data(delivery="courier")
    await cb.message.edit_text("🚚 Введите адрес доставки:")
    await cb.answer()


# === ВВОД АДРЕСА ===

@router.message(CheckoutFSM.address)
async def checkout_address(
    msg: Message,
    state: FSMContext,
    session: AsyncSession,
):
    data = await state.get_data()

    await OrdersDAO(session).set_delivery_address(
        user_id=msg.from_user.id,
        address=msg.text,
        delivery_method=data["delivery"],
    )

    await state.clear()
    await msg.answer(
        "Адрес сохранён.\n\nВыберите способ оплаты:",
        reply_markup=client_banks_kb(),
    )


# === ОПЛАТА ===

@router.callback_query(ClientPayBank.filter())
async def pay_bank(cb: CallbackQuery, callback_data: ClientPayBank):
    await cb.message.edit_text(
        f"🏦 Реквизиты банка #{callback_data.bank_id}\n\n"
        "После оплаты отправьте фото или PDF чека.",
    )
    await cb.answer()


@router.callback_query(ClientPaySBP.filter())
async def pay_sbp(cb: CallbackQuery):
    await cb.message.edit_text(
        "📱 Реквизиты СБП\n\n"
        "После оплаты отправьте фото или PDF чека.",
    )
    await cb.answer()


# === ОТМЕНА ===

@router.callback_query(ClientPaymentCancel.filter())
async def payment_cancel(cb: CallbackQuery):
    await cb.message.edit_text("❌ Оплата отменена")
    await cb.answer()