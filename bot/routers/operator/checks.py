# bot/routers/operator/checks.py
from aiogram import Router, F

# bot/routers/operator/checks.py
from aiogram import Router, F


from aiogram.types import CallbackQuery


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.orders_dao import OrdersDAO


from bot.dao.payment_dao import PaymentDAO





router = Router()





@router.callback_query(F.data.startswith("op:check:accept"))


async def accept(call: CallbackQuery, session: AsyncSession):


    order_id = int(call.data.split(":")[-1])


    await PaymentDAO(session).approve(order_id)


    await OrdersDAO(session).mark_paid(order_id)


    await session.commit()


    await call.message.edit_text("✅ Оплата подтверждена")





@router.callback_query(F.data.startswith("op:check:reject"))


async def reject(call: CallbackQuery, session: AsyncSession):


    order_id = int(call.data.split(":")[-1])


    await PaymentDAO(session).reject(payment_id=order_id, reason="Неверный чек")


    await session.commit()


    await call.message.edit_text("❌ Чек отклонён")





