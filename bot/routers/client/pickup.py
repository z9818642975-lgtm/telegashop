# bot/routers/client/pickup.py

# bot/routers/client/pickup.py
# bot/routers/client/pickup.py


from aiogram import Router


from aiogram.types import Message


from aiogram.fsm.context import FSMContext


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.orders_dao import OrdersDAO


from bot.fsm.checkout_fsm import CheckoutFSM


from bot.keyboards.payment import payment_method_kb


from bot.models.enums import OrderStatus





router = Router(name="client_pickup")








@router.message(CheckoutFSM.pickup_point)


async def choose_pickup_point(


    message: Message,


    state: FSMContext,


    session: AsyncSession,


    user,


):


    address = message.text.strip()





    order = await OrdersDAO(session).get_active(user.id)


    order.pickup_address = address


    order.status = OrderStatus.CHECKOUT_PAYMENT_METHOD


    await session.flush()





    await state.set_state(CheckoutFSM.payment)





    await message.answer(


        f"🏬 Самовывоз:\n{address}\n\n💳 Выберите способ оплаты",


        reply_markup=payment_method_kb(),


    )




