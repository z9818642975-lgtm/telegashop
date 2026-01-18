from __future__ import annotations

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from bot.models.order import Order
from bot.models.product import Product

router = Router(name="admin_reports")


@router.message(Command("report"))
async def report(
    message: Message,
    *,
    session: AsyncSession | None = None,
):
    orders_count = await session.scalar(
        select(func.count()).select_from(Order)
    )

    result = await session.execute(select(Product))
    products = result.scalars().all()

    text = (
        "📊 <b>Отчёт</b>\n\n"
        f"Всего заказов: {orders_count}\n\n"
        "📦 Остатки:\n"
    )

    for p in products:
        text += f"{p.name}: {p.stock}\n"

    await message.answer(text)

