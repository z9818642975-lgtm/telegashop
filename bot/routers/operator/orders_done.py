# bot/routers/operator/orders_done.py
from aiogram import Bot, F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.orders_dao import OrdersDAO
from bot.models.enums import OrderStatus
from bot.services.notifier import Notifier

router = Router(name="operator_orders_done")


@router.message(F.text == "О /done")
async def order_done(
    message: Message,
    session: AsyncSession,
    user,
    bot: Bot,
):
    orders = OrdersDAO(session)
    order = await orders.get_active_by_operator(user.id)

    if not order:
        await message.answer("❌ Нет активного заказа")
        return

    order.status = OrderStatus.DONE
    order.sla_deadline = None

    await session.commit()

    notifier = Notifier()
    await notifier.client(
        bot,
        order.client_tg_id,
        f"✅ Заказ #{order.id} выполнен"
    )

    await notifier.admin(
        bot,
        order.admin_tg_id,
        f"📦 Заказ #{order.id} закрыт оператором"
    )

    await message.answer(f"✅ Заказ #{order.id} закрыт")
