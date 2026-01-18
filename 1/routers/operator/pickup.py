from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.models.enums import UserRole
from bot.fsm.operator_pickup_fsm import OperatorPickupFSM
from bot.dao.orders_dao import OrdersDAO
from bot.services.pickup_timer import start_pickup_timer

router = Router(name="operator_pickup_ready")
router.message.filter(RoleFilter(UserRole.OPERATOR))
router.callback_query.filter(RoleFilter(UserRole.OPERATOR))


@router.callback_query(F.data.startswith("operator:op:ready:"))
async def start_ready(
    call: CallbackQuery,
    state: FSMContext | None = None,
):
    order_id = int(call.data.split(":")[-1])
    await state.update_data(order_id=order_id)
    await state.set_state(OperatorPickupFSM.comment)

    await call.message.answer("Р Р†РЎС™Р РЉР С—РЎвЂР РЏ Р В РЎвЂєР В РЎвЂ”Р В РЎвЂР РЋРІвЂљВ¬Р В РЎвЂР РЋРІР‚С™Р В Р’Вµ Р РЋР С“Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В·")
    await call.answer()


@router.message(OperatorPickupFSM.comment)
async def pickup_comment(message, *, state: FSMContext | None = None,
):
    await state.update_data(comment=message.text)
    await state.set_state(OperatorPickupFSM.photo)
    await message.answer("РЎР‚РЎСџРІР‚СљРЎвЂ Р В РЎвЂєР РЋРІР‚С™Р В РЎвЂ”Р РЋР вЂљР В Р’В°Р В Р вЂ Р РЋР Р‰Р РЋРІР‚С™Р В Р’Вµ Р РЋРІР‚С›Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂў")


@router.message(OperatorPickupFSM.photo, F.photo)
async def pickup_photo(message, *, state: FSMContext | None = None,
    session: AsyncSession | None = None,
):
    data = await state.get_data()
    order_id = data["order_id"]

    await OrdersDAO(session).set_operator_pickup_data(
        order_id=order_id,
        comment=data["comment"],
        photo_id=message.photo[-1].file_id,
    )

    start_pickup_timer(order_id)

    await session.commit()
    await state.clear()

    await message.answer("Р Р†РЎС™РІР‚В¦ Р В РЎв„ўР В Р’В»Р В РЎвЂР В Р’ВµР В Р вЂ¦Р РЋРІР‚С™ Р В Р’В±Р РЋРЎвЂњР В РўвЂР В Р’ВµР РЋРІР‚С™ Р РЋРЎвЂњР В Р вЂ Р В Р’ВµР В РўвЂР В РЎвЂўР В РЎВР В Р’В»Р РЋРІР‚ВР В Р вЂ¦ Р В Р’В°Р В Р вЂ Р РЋРІР‚С™Р В РЎвЂўР В РЎВР В Р’В°Р РЋРІР‚С™Р В РЎвЂР РЋРІР‚РЋР В Р’ВµР РЋР С“Р В РЎвЂќР В РЎвЂ")



