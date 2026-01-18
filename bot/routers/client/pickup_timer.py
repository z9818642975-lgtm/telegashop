# bot/routers/client/pickup_timer.py
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User
from bot.filters.role import RoleFilter
from bot.models.enums import UserRole, OrderStatus
from bot.dao.orders_dao import OrdersDAO
from bot.services.pickup_timer import start_pickup_timer
from bot.config import settings

router = Router(name="client_pickup_timer")
router.callback_query.filter(RoleFilter(UserRole.CLIENT))


@router.callback_query(F.data.startswith("client:pickup:timer:"))
async def start_timer(
    call: CallbackQuery,
    session: AsyncSession,
    user: User,
):
    order_id = int(call.data.split(":")[-1])
    orders = OrdersDAO(session)
    order = await orders.get(order_id)

    if not order or order.client_id != user.id:
        await call.answer("❌ Заказ не найден", show_alert=True)
        return

    if order.status not in (
        OrderStatus.PAYMENT_SUBMITTED,
        OrderStatus.ASSEMBLING,
        OrderStatus.READY,
    ):
        await call.answer("⏱ Таймер недоступен", show_alert=True)
        return

    # ⏱ запуск таймера (без дублей)
    start_pickup_timer(order_id)

    # 🔔 уведомляем оператора
    if order.operator_id:
        bot = Bot(settings.BOT_TOKEN)
        await bot.send_message(
            chat_id=order.operator_id,
            text=(
                f"⏱ Клиент нажал «10 минут»\n\n"
                f"📦 Заказ №{order.id}\n"
                f"Тип: {'Самовывоз' if order.delivery_type == 'pickup' else 'Доставка'}"
            ),
        )

    await call.answer("⏱ Таймер запущен")

