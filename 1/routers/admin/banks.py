from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.payment_dao import PaymentDAO
from bot.keyboards.admin.banks import banks_kb

router = Router(name="admin_banks")

# РІСњРЉ DISABLED (admin/operator text handler)
async def banks_entry(message, *, session: AsyncSession | None = None):
    dao = PaymentDAO(session)
    banks = await dao.list_requisites()
    if not banks:
        await message.answer("Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р’В Р В Р РЏР В РІР‚в„ўР вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В  Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРІР‚СњР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В° Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћ")
        return
    await message.answer("Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р’В Р В Р РЏР В РІР‚в„ўР вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљР’В", reply_markup=banks_kb(banks))

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:bank:toggle"))
async def bank_toggle(cb, *, session: AsyncSession | None = None):
    bank_id = int(cb.data.split(":")[-1])
    dao = PaymentDAO(session)
    await dao.toggle_bank(bank_id)
    await session.commit()
    banks = await dao.list_requisites()
    await cb.message.edit_reply_markup(reply_markup=banks_kb(banks))
    await cb.answer("OK")

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:bank:delete"))
async def bank_delete(cb, *, session: AsyncSession | None = None):
    bank_id = int(cb.data.split(":")[-1])
    dao = PaymentDAO(session)
    await dao.delete_bank(bank_id)
    await session.commit()
    banks = await dao.list_requisites()
    if banks:
        await cb.message.edit_reply_markup(reply_markup=banks_kb(banks))
    else:
        await cb.message.edit_text("Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р’В Р В Р РЏР В РІР‚в„ўР вЂ™Р’В¦ Р В Р’В Р вЂ™Р’В Р В Р вЂ Р В РІР‚С™Р вЂ™Р’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎСљР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В  Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В±Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р В Р вЂ№Р В Р’В Р В РІР‚В°Р В Р’В Р В Р вЂ№Р В Р вЂ Р Р†Р вЂљРЎв„ўР вЂ™Р’В¬Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’Вµ Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р В Р вЂ№Р В Р вЂ Р В РІР‚С™Р РЋРІвЂћСћ")
    await cb.answer("Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†РІР‚С™Р’В¬Р В Р’В Р вЂ™Р’В Р В РЎС›Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’ВµР В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›")



