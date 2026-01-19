from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.orders_dao import OrdersDAO
from bot.dao.bank_accounts_dao import BankAccountsDAO

router = Router(name="client_payment")


# =========================================================
# CHOOSE PAYMENT METHOD (BANK / SBP)
# =========================================================

@router.callback_query(F.data.startswith("client:pay:"))
async def choose_payment_method(
    cb: CallbackQuery,
    session: AsyncSession,
    user,
):
    data = cb.data

    orders = OrdersDAO(session)
    order = await orders.get_cart(user.id)

    if not order:
        await cb.answer("Корзина пуста", show_alert=True)
        return

    # -------------------------
    # BANK (pay:bank:<bank_id>)
    # -------------------------
    if data.startswith("client:pay:bank:"):
        bank_id = int(data.split(":")[2])

        bank = await BankAccountsDAO(session).get_by_id(bank_id)
        if not bank:
            await cb.answer("Банк не найден", show_alert=True)
            return

        order.bank_account_id = bank.id
        await session.flush()

        await cb.message.edit_text(
            (
                "💳 <b>Реквизиты для оплаты</b>\n\n"
                f"{bank.requisites}\n\n"
                "После оплаты нажмите «Я оплатил»."
            ),
            reply_markup=None,
        )
        return

    # -------------------------
    # SBP (pay:sbp)
    # -------------------------
    if data == CB.PAY_SBP:
        await cb.message.edit_text(
            (
                "💳 <b>Оплата через СБП</b>\n\n"
                "Переведите средства по номеру телефона.\n\n"
                "После оплаты нажмите «Я оплатил»."
            ),
            reply_markup=None,
        )
        return

    await cb.answer("Неизвестный способ оплаты", show_alert=True)
