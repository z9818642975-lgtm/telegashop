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


@router.callback_query(F.data.startswith("operator:ready:"))
async def start_ready(
    call: CallbackQuery,
    state: FSMContext,
):
    order_id = int(call.data.split(":")[-1])
    await state.update_data(order_id=order_id)
    await state.set_state(OperatorPickupFSM.comment)

    await call.message.answer("✍️ Опишите самовывоз")
    await call.answer()


@router.message(OperatorPickupFSM.comment)
async def pickup_comment(
    message: Message,
    state: FSMContext,
):
    await state.update_data(comment=message.text)
    await state.set_state(OperatorPickupFSM.photo)
    await message.answer("📸 Отправьте фото")


@router.message(OperatorPickupFSM.photo, F.photo)
async def pickup_photo(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
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

    await message.answer("✅ Клиент будет уведомлён автоматически")

