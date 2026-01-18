from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.statistics_dao import StatisticsDAO

router = Router(name="admin_statistics")

@router.callback_query(RoleFilter("admin"), F.data == "admin:stats:week")
async def stats_week(cb: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    d = await dao.period_summary(days=7)
    await cb.message.edit_text(
        "📊 <b>Неделя</b>\n\n"
        f"📦 {d['orders_total']}\n"
        f"✅ {d['orders_paid']}\n"
        f"💰 {d['revenue']} ₽\n"
        f"🧾 {d['avg_check']} ₽",
        parse_mode="HTML",
    )
    await cb.answer()

@router.callback_query(RoleFilter("admin"), F.data == "admin:stats:month")
async def stats_month(cb: CallbackQuery, session: AsyncSession):
    dao = StatisticsDAO(session)
    d = await dao.period_summary(days=30)
    await cb.message.edit_text(
        "📊 <b>Месяц</b>\n\n"
        f"📦 {d['orders_total']}\n"
        f"✅ {d['orders_paid']}\n"
        f"💰 {d['revenue']} ₽\n"
        f"🧾 {d['avg_check']} ₽",
        parse_mode="HTML",
    )
    await cb.answer()

