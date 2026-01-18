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








# ❌ DISABLED (admin/operator text handler)
async def start_shift_or_request_address(message, *, session: AsyncSession | None = None,


    state: FSMContext | None = None,


    user,


):


    warehouses = WarehousesDAO(session)


    shifts = OperatorShiftDAO(session)





    wh = await warehouses.get_operator_wh(user.id)





    if wh and wh.address:


        # Р В Р’В°Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“ Р РЋРЎвЂњР В Р’В¶Р В Р’Вµ Р В Р’ВµР РЋР С“Р РЋРІР‚С™Р РЋР Р‰ Р Р†РІР‚В РІР‚в„ў Р РЋР С“Р РЋР вЂљР В Р’В°Р В Р’В·Р РЋРЎвЂњ Р РЋР С“Р РЋРІР‚С™Р В Р’В°Р РЋР вЂљР РЋРІР‚С™Р РЋРЎвЂњР В Р’ВµР В РЎВ Р РЋР С“Р В РЎВР В Р’ВµР В Р вЂ¦Р РЋРЎвЂњ


        await shifts.start_shift(


            operator_id=user.id,


            pickup_address=wh.address,


        )


        await session.commit()





        await message.answer(


            f"Р Р†РЎС™РІР‚В¦ Р В Р Р‹Р В РЎВР В Р’ВµР В Р вЂ¦Р В Р’В° Р В Р вЂ¦Р В Р’В°Р РЋРІР‚РЋР В Р’В°Р РЋРІР‚С™Р В Р’В°\nРЎР‚РЎСџРІР‚СљР РЉ Р В Р Р‹Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В·:\n{wh.address}",


            reply_markup=on_shift_kb(),


        )


        return





    # Р В Р’В°Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“Р В Р’В° Р В Р вЂ¦Р В Р’ВµР РЋРІР‚С™ Р Р†РІР‚В РІР‚в„ў Р В Р’В·Р В Р’В°Р В РЎвЂ”Р РЋР вЂљР В Р’В°Р РЋРІвЂљВ¬Р В РЎвЂР В Р вЂ Р В Р’В°Р В Р’ВµР В РЎВ Р В Р вЂ Р В Р вЂ Р В РЎвЂўР В РўвЂ


    await state.set_state(OperatorPickupState.waiting_for_address)


    await message.answer(


        "РЎР‚РЎСџРІР‚СљР РЉ Р В РІР‚в„ўР В Р вЂ Р В Р’ВµР В РўвЂР В РЎвЂР РЋРІР‚С™Р В Р’Вµ Р В Р’В°Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“ Р РЋР С“Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В·Р В Р’В° Р В РЎвЂўР В РўвЂР В Р вЂ¦Р В РЎвЂР В РЎВ Р РЋР С“Р В РЎвЂўР В РЎвЂўР В Р’В±Р РЋРІР‚В°Р В Р’ВµР В Р вЂ¦Р В РЎвЂР В Р’ВµР В РЎВ:"


    )








@router.message(


    RoleFilter("operator"),


    OperatorPickupState.waiting_for_address,


)


async def save_pickup_address(message, *, session: AsyncSession | None = None,


    state: FSMContext | None = None,


    user,


):


    address = message.text.strip()





    if len(address) < 5:


        await message.answer("Р Р†РЎСљР Р‰ Р В РЎвЂ™Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“ Р РЋР С“Р В Р’В»Р В РЎвЂР РЋРІвЂљВ¬Р В РЎвЂќР В РЎвЂўР В РЎВ Р В РЎвЂќР В РЎвЂўР РЋР вЂљР В РЎвЂўР РЋРІР‚С™Р В РЎвЂќР В РЎвЂР В РІвЂћвЂ“, Р В РЎвЂ”Р В РЎвЂўР В РЎвЂ”Р РЋР вЂљР В РЎвЂўР В Р’В±Р РЋРЎвЂњР В РІвЂћвЂ“Р РЋРІР‚С™Р В Р’Вµ Р В Р’ВµР РЋРІР‚В°Р РЋРІР‚В Р РЋР вЂљР В Р’В°Р В Р’В·")


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


        f"Р Р†РЎС™РІР‚В¦ Р В РЎвЂ™Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“ Р РЋР С“Р В РЎвЂўР РЋРІР‚В¦Р РЋР вЂљР В Р’В°Р В Р вЂ¦Р РЋРІР‚ВР В Р вЂ¦\nРЎР‚РЎСџРІР‚СљР РЉ Р В Р Р‹Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В·:\n{address}\n\nР В Р Р‹Р В РЎВР В Р’ВµР В Р вЂ¦Р В Р’В° Р В Р вЂ¦Р В Р’В°Р РЋРІР‚РЋР В Р’В°Р РЋРІР‚С™Р В Р’В°",


        reply_markup=on_shift_kb(),


    )







