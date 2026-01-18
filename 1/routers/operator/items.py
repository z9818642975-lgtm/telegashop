# bot/routers/operator/items.py
from aiogram import Router, F

# bot/routers/operator/items.py
from aiogram import Router, F


from aiogram.types import Message


from aiogram.fsm.context import FSMContext


from sqlalchemy.ext.asyncio import AsyncSession





from bot.filters.role import RoleFilter


from bot.models.enums import UserRole


from bot.models.user import User


from bot.dao.order_items import OrderItemDAO


from bot.services.operator_guard import ensure_operator_owns_item


from bot.fsm.operator_item_fsm import OperatorItemFSM





from bot.middlewares.shift_guard import ShiftGuardMiddleware





router = Router(name="operator_items")





router.message.middleware(ShiftGuardMiddleware())





router.message.filter(RoleFilter(UserRole.OPERATOR))








@router.message(F.text.startswith("/accept "))


async def accept_item_handler(message, *, state: FSMContext | None = None,


    session: AsyncSession | None = None,


    user: User,


):


    try:


        item_id = int(message.text.split()[1])





        item = await OrderItemDAO.accept(


            session=session,


            item_id=item_id,


            operator_id=user.id,


        )


        await session.commit()





    except Exception as e:


        await session.rollback()


        await message.answer(f"Р Р†РЎСљР Р‰ {e}")


        return





    await state.set_state(OperatorItemFSM.accepted)


    await state.update_data(item_id=item.id)


    await message.answer(f"Р Р†РЎС™РІР‚В¦ Р В РЎСџР В РЎвЂўР В Р’В·Р В РЎвЂР РЋРІР‚В Р В РЎвЂР РЋР РЏ #{item.id} Р В РЎвЂ”Р РЋР вЂљР В РЎвЂР В Р вЂ¦Р РЋР РЏР РЋРІР‚С™Р В Р’В°")








# ❌ DISABLED (text-based handler)
async def paid_handler(message, *, state: FSMContext | None = None,


    session: AsyncSession | None = None,


    user: User,


):


    data = await state.get_data()





    try:


        item = await OrderItemDAO.mark_paid(


            session=session,


            item_id=data["item_id"],


        )





        await ensure_operator_owns_item(


            session=session,


            operator_id=user.id,


            item_id=item.id,


        )





        await session.commit()





    except Exception as e:


        await session.rollback()


        await message.answer(f"Р Р†РЎСљР Р‰ {e}")


        return





    await state.set_state(OperatorItemFSM.paid)


    await message.answer("РЎР‚РЎСџРІР‚в„ўР’В° Р В РЎвЂєР В РЎвЂ”Р В Р’В»Р В Р’В°Р РЋРІР‚С™Р В Р’В° Р В РЎвЂ”Р В РЎвЂўР В РўвЂР РЋРІР‚С™Р В Р вЂ Р В Р’ВµР РЋР вЂљР В Р’В¶Р В РўвЂР В Р’ВµР В Р вЂ¦Р В Р’В°")








# ❌ DISABLED (text-based handler)
async def done_handler(message, *, state: FSMContext | None = None,


    session: AsyncSession | None = None,


    user: User,


):


    data = await state.get_data()





    try:


        item = await OrderItemDAO.complete(


            session=session,


            item_id=data["item_id"],


        )





        await ensure_operator_owns_item(


            session=session,


            operator_id=user.id,


            item_id=item.id,


        )





        await session.commit()





    except Exception as e:


        await session.rollback()


        await message.answer(f"Р Р†РЎСљР Р‰ {e}")


        return





    await state.clear()


    await message.answer(


        "РЎР‚РЎСџР РЏР С“ Р В РЎСџР В РЎвЂўР В Р’В·Р В РЎвЂР РЋРІР‚В Р В РЎвЂР РЋР РЏ Р В Р’В·Р В Р’В°Р В Р вЂ Р В Р’ВµР РЋР вЂљР РЋРІвЂљВ¬Р В Р’ВµР В Р вЂ¦Р В Р’В°\n"


        "РЎР‚РЎСџРІР‚в„ўРЎвЂ Р В РІР‚вЂќР В Р’В°Р РЋР вЂљР В РЎвЂ”Р В Р’В»Р В Р’В°Р РЋРІР‚С™Р В Р’В° Р В Р вЂ¦Р В Р’В°Р РЋРІР‚РЋР В РЎвЂР РЋР С“Р В Р’В»Р В Р’ВµР В Р вЂ¦Р В Р’В°"


    )







