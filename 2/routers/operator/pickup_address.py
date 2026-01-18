# bot/routers/operator/pickup_address.py
from aiogram import Router, F

# bot/routers/operator/pickup_address.py
from aiogram import Router, F


from aiogram.types import Message


from aiogram.fsm.context import FSMContext


from sqlalchemy.ext.asyncio import AsyncSession





from bot.filters.role import RoleFilter


from bot.states.operator_pickup import OperatorPickupState


from bot.dao.warehouses_dao import WarehousesDAO


from bot.dao.operator_shift_dao import OperatorShiftDAO


from bot.keyboards.operator.shift import on_shift_kb





router = Router(name="operator_pickup_address")








@router.message(RoleFilter("operator"), F.text == "🟢 Начать смену")


async def start_shift_or_request_address(


    message: Message,


    session: AsyncSession,


    state: FSMContext,


    user,


):


    warehouses = WarehousesDAO(session)


    shifts = OperatorShiftDAO(session)





    wh = await warehouses.get_operator_wh(user.id)





    if wh and wh.address:


        # адрес уже есть → сразу стартуем смену


        await shifts.start_shift(


            operator_id=user.id,


            pickup_address=wh.address,


        )


        await session.commit()





        await message.answer(


            f"✅ Смена начата\n📍 Самовывоз:\n{wh.address}",


            reply_markup=on_shift_kb(),


        )


        return





    # адреса нет → запрашиваем ввод


    await state.set_state(OperatorPickupState.waiting_for_address)


    await message.answer(


        "📍 Введите адрес самовывоза одним сообщением:"


    )








@router.message(


    RoleFilter("operator"),


    OperatorPickupState.waiting_for_address,


)


async def save_pickup_address(


    message: Message,


    session: AsyncSession,


    state: FSMContext,


    user,


):


    address = message.text.strip()





    if len(address) < 5:


        await message.answer("❌ Адрес слишком короткий, попробуйте ещё раз")


        return





    warehouses = WarehousesDAO(session)


    shifts = OperatorShiftDAO(session)





    await warehouses.set_operator_address(


        operator_id=user.id,


        address=address,


    )





    await shifts.start_shift(


        operator_id=user.id,


        pickup_address=address,


    )





    await session.commit()


    await state.clear()





    await message.answer(


        f"✅ Адрес сохранён\n📍 Самовывоз:\n{address}\n\nСмена начата",


        reply_markup=on_shift_kb(),


    )





