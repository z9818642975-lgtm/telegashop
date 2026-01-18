from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.salary_dao import SalaryDAO

router = Router(name="operator_salary")


# =========================================================
# 💰 МОЯ ЗАРПЛАТА
# =========================================================
@router.message(RoleFilter("operator"), F.text == "💰 Зарплата")
async def my_salary(
    message: Message,
    session: AsyncSession,
    user,
):
    if not user:
        await message.answer("❌ Пользователь не найден")
        return

    salary_dao = SalaryDAO(session)
    rows = await salary_dao.list_by_operator(user.id)

    if not rows:
        await message.answer("💸 Начислений пока нет")
        return

    total = 0
    text = "💰 <b>Моя зарплата</b>\n\n"

    for r in rows:
        total += r.amount
        text += (
            f"🧾 Заказ: {r.order_id or '—'}\n"
            f"💵 Сумма: {r.amount} ₽\n"
            f"📌 Статус: {r.status}\n"
            f"⏱ {r.created_at:%d.%m %H:%M}\n\n"
        )

    text += f"<b>Итого к выплате:</b> {total} ₽"

    await message.answer(text)


# =========================================================
# 📤 ЗАПРОСИТЬ ВЫПЛАТУ
# =========================================================
@router.message(RoleFilter("operator"), F.text == "📤 Запросить выплату")
async def request_payout(
    message: Message,
    session: AsyncSession,
    user,
):
    if not user:
        await message.answer("❌ Пользователь не найден")
        return

    salary_dao = SalaryDAO(session)
    await salary_dao.request_payout(user.id)
    await session.commit()

    await message.answer("📤 Запрос на выплату отправлен")

