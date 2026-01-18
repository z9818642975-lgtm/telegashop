from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.models.order import Order
from bot.models.enums import OrderStatus

router = Router(name="operator_orders")


@router.message(Command("orders"))
async def list_orders(
    message: Message,
    *,
    session: AsyncSession | None = None,
):
    """
    Список заказов, ожидающих подтверждения оператором.
    """

    if session is None:
        await message.answer("⚠️ Нет подключения к базе данных")
        return

    result = await session.execute(
        select(Order).where(Order.status == OrderStatus.PAID_PENDING)
    )
    orders = result.scalars().all()

    if not orders:
        await message.answer("📭 Нет заказов для подтверждения.")
        return

    lines = ["📋 Заказы на подтверждение:\n"]
    for order in orders:
        lines.append(f"• Заказ #{order.id} от пользователя {order.client_id}")

    await message.answer("\n".join(lines))

