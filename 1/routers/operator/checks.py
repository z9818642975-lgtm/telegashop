# bot/routers/operator/checks.py
from aiogram import Router, F

# bot/routers/operator/checks.py
from aiogram import Router, F


from aiogram.types import CallbackQuery


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.orders_dao import OrdersDAO


from bot.dao.payment_dao import PaymentDAO





router = Router()





@router.callback_query(F.data.startswith("operator:op:check:accept"))


async def accept(call: CallbackQuery, session: AsyncSession | None = None):


    order_id = int(call.data.split(":")[-1])


    await PaymentDAO(session).approve(order_id)


    await OrdersDAO(session).mark_paid(order_id)


    await session.commit()


    await call.message.edit_text("Р Р†РЎС™РІР‚В¦ Р В РЎвЂєР В РЎвЂ”Р В Р’В»Р В Р’В°Р РЋРІР‚С™Р В Р’В° Р В РЎвЂ”Р В РЎвЂўР В РўвЂР РЋРІР‚С™Р В Р вЂ Р В Р’ВµР РЋР вЂљР В Р’В¶Р В РўвЂР В Р’ВµР В Р вЂ¦Р В Р’В°")





@router.callback_query(F.data.startswith("operator:op:check:reject"))


async def reject(call: CallbackQuery, session: AsyncSession | None = None):


    order_id = int(call.data.split(":")[-1])


    await PaymentDAO(session).reject(payment_id=order_id, reason="Р В РЎСљР В Р’ВµР В Р вЂ Р В Р’ВµР РЋР вЂљР В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІР‚РЋР В Р’ВµР В РЎвЂќ")


    await session.commit()


    await call.message.edit_text("Р Р†РЎСљР Р‰ Р В Р’В§Р В Р’ВµР В РЎвЂќ Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂќР В Р’В»Р В РЎвЂўР В Р вЂ¦Р РЋРІР‚ВР В Р вЂ¦")






