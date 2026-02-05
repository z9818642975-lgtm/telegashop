# bot/services/operator_shift_watcher.py
import asyncio
import logging

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.services.notifier import Notifier

logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 60


async def operator_shift_watcher(
    bot: Bot,
    sessionmaker: async_sessionmaker,
) -> None:
    logger.info("👁 operator_shift_watcher started")

    notifier = Notifier(bot)

    while True:
        try:
            async with sessionmaker() as session:
                dao = OperatorShiftDAO(session)

                # 15 минут → предупреждение (осталось ~5)
                for shift in await dao.get_active_older_than(15):
                    if not shift.warned_15:
                        await notifier.notify_operator_shift_ending(
                            operator_tg_id=shift.operator_id,
                            minutes_left=5,
                        )
                        await dao.mark_warned(shift.id, 15)

                # 17 минут → предупреждение (осталось ~3)
                for shift in await dao.get_active_older_than(17):
                    if not shift.warned_17:
                        await notifier.notify_operator_shift_ending(
                            operator_tg_id=shift.operator_id,
                            minutes_left=3,
                        )
                        await dao.mark_warned(shift.id, 17)

                # 20 минут → автозакрытие
                for shift in await dao.get_active_older_than(20):
                    if not shift.auto_closed:
                        await notifier.notify_operator_shift_closed(
                            operator_tg_id=shift.operator_id,
                        )
                        await dao.mark_warned(shift.id, 20)
                        await dao.stop_by_id(shift.id, auto=True)

                await session.commit()

        except Exception:
            logger.exception("🔥 operator_shift_watcher error")

        await asyncio.sleep(CHECK_INTERVAL_SECONDS)
