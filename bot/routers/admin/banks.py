# bot/routers/admin/banks.py
from aiogram import Router
from aiogram.types import CallbackQuery

from bot.constants.callbacks_admin import AdminBanks, AdminBankToggle
from bot.dao.bank_accounts_dao import BankAccountsDAO
from bot.keyboards.admin.banks import admin_banks_kb

router = Router(name="admin_banks")


@router.callback_query(AdminBanks.filter())
async def admin_banks(cb: CallbackQuery):
    dao = BankAccountsDAO()
    banks = await dao.list_all()

    await cb.message.edit_text(
        "🏦 <b>Банки</b>",
        reply_markup=admin_banks_kb(banks),
    )
    await cb.answer()


@router.callback_query(AdminBankToggle.filter())
async def bank_toggle(
    cb: CallbackQuery,
    callback_data: AdminBankToggle,
):
    dao = BankAccountsDAO()
    await dao.toggle(callback_data.bank_id)
    await cb.answer("Статус банка изменён")

