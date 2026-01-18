from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.orders import OrdersDAO

router = Router(name="client_checkout")

# ❌ DISABLED (text-based handler)
async def checkout(message: Message, *, session: AsyncSession | None = None, user):
    await message.answer("РЎР‚РЎСџРІР‚СљР вЂ№ Р В РЎСџР РЋР вЂљР В РЎвЂР РЋРІвЂљВ¬Р В Р’В»Р В РЎвЂР РЋРІР‚С™Р В Р’Вµ Р РЋРІР‚С›Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂў Р В РЎвЂР В Р’В»Р В РЎвЂ Р РЋРІР‚С›Р В Р’В°Р В РІвЂћвЂ“Р В Р’В» Р РЋРІР‚РЋР В Р’ВµР В РЎвЂќР В Р’В°.")

@router.message(F.photo)
async def upload_receipt(message: Message, *, session: AsyncSession | None = None, user):
    order = await OrdersDAO.get_draft(session, user.id)
    await OrdersDAO.submit(
        session,
        order,
        receipt_id=message.photo[-1].file_id,
    )
    await message.answer("Р Р†РЎС™РІР‚В¦ Р В Р’В§Р В Р’ВµР В РЎвЂќ Р В РЎвЂ”Р В РЎвЂўР В Р’В»Р РЋРЎвЂњР РЋРІР‚РЋР В Р’ВµР В Р вЂ¦. Р В РЎвЂєР В Р’В¶Р В РЎвЂР В РўвЂР В Р’В°Р В РІвЂћвЂ“Р РЋРІР‚С™Р В Р’Вµ Р В РЎвЂ”Р В РЎвЂўР В РўвЂР РЋРІР‚С™Р В Р вЂ Р В Р’ВµР РЋР вЂљР В Р’В¶Р В РўвЂР В Р’ВµР В Р вЂ¦Р В РЎвЂР РЋР РЏ Р В РЎвЂўР В РЎвЂ”Р В Р’ВµР РЋР вЂљР В Р’В°Р РЋРІР‚С™Р В РЎвЂўР РЋР вЂљР В Р’В°.")


