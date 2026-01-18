# bot/routers/client/payment_confirm.py
from aiogram import Router, F

# bot/routers/client/payment_confirm.py
from aiogram import Router, F


from aiogram.types import CallbackQuery, Message


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.orders_dao import OrdersDAO


from bot.models.enums import OrderStatus


from bot.models.user import User


from bot.services.order_service import OrderService


from bot.keyboards.client.main import client_main_menu





router = Router(name="client_payment_confirm")








@router.callback_query(F.data == "payment:submit")


async def submit(


    cb: CallbackQuery,


    session: AsyncSession,


    user: User,


):


    await cb.message.answer(


        "📎 Пришлите чек (скриншот или PDF)"


    )








@router.message(F.photo | F.document)


async def receive_receipt(


    message: Message,


    session: AsyncSession,


    user: User,


):


    order = await OrdersDAO(session).get_active(user.id)


    if not order or order.status != OrderStatus.WAITING_PAYMENT:


        return





    await OrderService.submit_payment(order.id, message, session)





    await message.answer(


        "✅ Чек получен. Ожидайте подтверждения оператора."


    )








@router.callback_query(F.data == "payment:cancel")


async def cancel(


    cb: CallbackQuery,


    session: AsyncSession,


    user: User,


):


    order = await OrdersDAO(session).get_active(user.id)


    if not order:


        return





    await OrderService.cancel_order(order.id, session)





    await cb.message.answer(


        "❌ Заказ отменён",


        reply_markup=client_main_menu(),


    )





