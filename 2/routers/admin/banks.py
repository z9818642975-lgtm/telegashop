from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.payment_dao import PaymentDAO
from bot.keyboards.admin.banks import banks_kb

router = Router(name="admin_banks")

@router.message(RoleFilter("admin"), F.text == "🏦 Банки")
async def banks_entry(message: Message, session: AsyncSession):
    dao = PaymentDAO(session)
    banks = await dao.list_requisites()
    if not banks:
        await message.answer("🏦 Банков пока нет")
        return
    await message.answer("🏦 Банки", reply_markup=banks_kb(banks))

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:bank:toggle"))
async def bank_toggle(cb: CallbackQuery, session: AsyncSession):
    bank_id = int(cb.data.split(":")[-1])
    dao = PaymentDAO(session)
    await dao.toggle_bank(bank_id)
    await session.commit()
    banks = await dao.list_requisites()
    await cb.message.edit_reply_markup(reply_markup=banks_kb(banks))
    await cb.answer("OK")

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:bank:delete"))
async def bank_delete(cb: CallbackQuery, session: AsyncSession):
    bank_id = int(cb.data.split(":")[-1])
    dao = PaymentDAO(session)
    await dao.delete_bank(bank_id)
    await session.commit()
    banks = await dao.list_requisites()
    if banks:
        await cb.message.edit_reply_markup(reply_markup=banks_kb(banks))
    else:
        await cb.message.edit_text("🏦 Банков больше нет")
    await cb.answer("Удалено")

