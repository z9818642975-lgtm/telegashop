# bot/routers/operator/delivery.py
from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import settings
from bot.constants.callbacks_operator import OperatorDeliveryStartCB
from bot.dao.orders_dao import OrdersDAO
from bot.filters.role import RoleFilter
from bot.fsm.operator_delivery_fsm import OperatorDeliveryFSM
from bot.models.enums import OrderStatus, UserRole
from bot.models.user import User

router = Router(name="operator_delivery")
router.message.filter(RoleFilter(UserRole.OPERATOR))
router.callback_query.filter(RoleFilter(UserRole.OPERATOR))


@router.callback_query(OperatorDeliveryStartCB.filter())
async def delivery_start(
    call: CallbackQuery,
    callback_data: OperatorDeliveryStartCB,
    state: FSMContext,
):
    await state.set_state(OperatorDeliveryFSM.track)
    await state.update_data(order_id=callback_data.order_id)
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