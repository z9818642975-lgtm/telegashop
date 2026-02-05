# bot/routers/admin/statistics.py
from aiogram import F, Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.statistics_dao import StatisticsDAO
from bot.filters.role import RoleFilter
from bot.utils.safe_edit import safe_edit_text

router = Router(name="admin_statistics")

@router.callback_query(RoleFilter("admin"), F.data == "admin:stats:week")
async def stats_week(cb: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    d = await dao.period_summary(days=7)

    await safe_edit_text(
        cb.message,
        text=(
            "📊 <b>Неделя</b>\n\n"
            f"📦 {d['orders_total']}\n"
            f"✅ {d['orders_paid']}\n"
            f"💰 {d['revenue']} ₽\n"
            f"🧾 {d['avg_check']} ₽"
        ),
        parse_mode="HTML",
    )
    await cb.answer()

@router.callback_query(RoleFilter("admin"), F.data == "admin:stats:month")
async def stats_month(cb: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    d = await dao.period_summary(days=30)

    await safe_edit_text(
        cb.message,
        text=(
            "📊 <b>Месяц</b>\n\n"
            f"📦 {d['orders_total']}\n"
            f"✅ {d['orders_paid']}\n"
            f"💰 {d['revenue']} ₽\n"
            f"🧾 {d['avg_check']} ₽"
        ),
        parse_mode="HTML",
    )
    await cb.answer()

