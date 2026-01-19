# bot/routers/operator/delivery.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.models.enums import UserRole, OrderStatus
from bot.models.user import User
from bot.dao.orders_dao import OrdersDAO
from bot.fsm.operator_delivery_fsm import OperatorDeliveryFSM
from bot.config import settings
from aiogram import Bot

router = Router(name="operator_delivery")
router.message.filter(RoleFilter(UserRole.OPERATOR))
router.callback_query.filter(RoleFilter(UserRole.OPERATOR))


@router.callback_query(F.data.startswith("operator:delivery:sent:"))
async def delivery_start(
    call: CallbackQuery,
    state: FSMContext,
):
    order_id = int(call.data.split(":")[-1])
    await state.set_state(OperatorDeliveryFSM.track)
    await state.update_data(order_id=order_id)
    await call.message.answer("🔗 Введите трек-ссылку")
    await call.answer()


@router.message(OperatorDeliveryFSM.track)
async def delivery_track(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User,
):
    data = await state.get_data()
    order_id = data["order_id"]
    track = message.text.strip()

    order = await OrdersDAO(session).get(order_id)
    if not order:
        await state.clear()
        return

    order.status = OrderStatus.SENT
    await session.commit()

    bot = Bot(settings.BOT_TOKEN)
    await bot.send_message(
        chat_id=order.client_id,
        text=f"🚚 Заказ передан курьеру\n\n🔗 Трек:\n{track}",
    )

    await state.clear()
    await message.answer("✅ Трек отправлен клиенту")

