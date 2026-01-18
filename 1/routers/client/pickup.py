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


async def choose_pickup_point(message, *, state: FSMContext | None = None,


    session: AsyncSession | None = None,


    user,


):


    address = message.text.strip()





    order = await OrdersDAO(session).get_active(user.id)


    order.pickup_address = address


    order.status = OrderStatus.CHECKOUT_PAYMENT_METHOD


    await session.flush()





    await state.set_state(CheckoutFSM.payment)





    await message.answer(


        f"Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ Р В Р’В Р В Р вЂ№Р В Р’В Р вЂ™Р’В°Р В Р’В Р РЋР’ВР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В·:\n{address}\n\nР РЋР вЂљР РЋРЎСџР Р†Р вЂљРІвЂћСћР РЋРІР‚вЂњ Р В Р’В Р Р†Р вЂљРІвЂћСћР В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РІР‚С™Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’Вµ Р В Р Р‹Р В РЎвЂњР В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р Р‹Р В РЎвЂњР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В± Р В Р’В Р РЋРІР‚СћР В Р’В Р РЋРІР‚вЂќР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р Р†Р вЂљРІвЂћвЂ“",


        reply_markup=payment_method_kb(),


    )






