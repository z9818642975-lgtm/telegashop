from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.statistics_dao import StatisticsDAO

router = Router(name="admin_statistics")

@router.callback_query(RoleFilter("admin"), F.data == "admin:stats:week")
async def stats_week(cb, *, session: AsyncSession | None = None):
    dao = StatisticsDAO(session)
    d = await dao.period_summary(days=7)
    await cb.message.edit_text(
        "Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р В РІР‚В° <b>Р В Р’В Р РЋРЎС™Р В Р’В Р вЂ™Р’ВµР В Р’В Р СћРІР‚ВР В Р’В Р вЂ™Р’ВµР В Р’В Р вЂ™Р’В»Р В Р Р‹Р В Р РЏ</b>\n\n"
        f"Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р вЂ™Р’В¦ {d['orders_total']}\n"
        f"Р В Р вЂ Р РЋРЎв„ўР Р†Р вЂљР’В¦ {d['orders_paid']}\n"
        f"Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРІвЂћСћР вЂ™Р’В° {d['revenue']} Р В Р вЂ Р Р†Р вЂљРЎв„ўР В РІР‚В¦\n"
        f"Р РЋР вЂљР РЋРЎСџР вЂ™Р’В§Р РЋРІР‚Сћ {d['avg_check']} Р В Р вЂ Р Р†Р вЂљРЎв„ўР В РІР‚В¦",
        parse_mode="HTML",
    )
    await cb.answer()

@router.callback_query(RoleFilter("admin"), F.data == "admin:stats:month")
async def stats_month(cb, *, session: AsyncSession | None = None):
    dao = StatisticsDAO(session)
    d = await dao.period_summary(days=30)
    await cb.message.edit_text(
        "Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р В РІР‚В° <b>Р В Р’В Р РЋРЎв„ўР В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РЎвЂњР В Р Р‹Р В Р РЏР В Р Р‹Р Р†Р вЂљР’В </b>\n\n"
        f"Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р вЂ™Р’В¦ {d['orders_total']}\n"
        f"Р В Р вЂ Р РЋРЎв„ўР Р†Р вЂљР’В¦ {d['orders_paid']}\n"
        f"Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРІвЂћСћР вЂ™Р’В° {d['revenue']} Р В Р вЂ Р Р†Р вЂљРЎв„ўР В РІР‚В¦\n"
        f"Р РЋР вЂљР РЋРЎСџР вЂ™Р’В§Р РЋРІР‚Сћ {d['avg_check']} Р В Р вЂ Р Р†Р вЂљРЎв„ўР В РІР‚В¦",
        parse_mode="HTML",
    )
    await cb.answer()



