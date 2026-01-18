# bot/services/operator_shift_watcher.py
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.dao.operator_shift_dao import OperatorShiftDAO

logger = logging.getLogger("telegashop")


async def operator_shift_watcher(
    *,
    bot: Bot,
    sessionmaker: async_sessionmaker,
):
    """
    Фоновый watchdog:
    - 15 мин → warn
    - 17 мин → warn
    - 20 мин → auto close
    """

    logger.info("👁 operator_shift_watcher started")

    while True:
        try:
            async with sessionmaker() as session:
                dao = OperatorShiftDAO(session)

                # --- 20 минут → автозакрытие
                shifts_20 = await dao.get_stale_shifts(
                    inactive_minutes=dao.AUTO_CLOSE_MINUTES
                )
                for shift in shifts_20:
                    await dao.stop_shift_by_id(shift_id=shift.id)

                    logger.warning(
                        f"⛔ Operator {shift.operator_id} shift auto-closed (20 min)"
                    )

                # --- 17 минут → предупреждение
                shifts_17 = await dao.get_stale_shifts(
                    inactive_minutes=dao.WARN_17_MINUTES
                )
                for shift in shifts_17:
                    await dao.mark_warned(shift.id, minutes=17)

                # --- 15 минут → предупреждение
                shifts_15 = await dao.get_stale_shifts(
                    inactive_minutes=dao.WARN_15_MINUTES
                )
                for shift in shifts_15:
                    await dao.mark_warned(shift.id, minutes=15)

                await session.commit()

        except Exception:
            logger.exception("🔥 operator_shift_watcher error")

        await asyncio.sleep(60)
