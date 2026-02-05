# bot/services/operator_monitor.DISABLED.py
#C:\Users\1\project\bot\services\operator_monitor.py

# bot/services/operator_monitor.py
#C:\Users\1\project\bot\services\operator_monitor.py


from __future__ import annotations

import asyncio
import logging

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.dao.operator_shift_dao import OperatorShiftDAO

logger = logging.getLogger("telegashop")





INACTIVE_AFTER_MINUTES = 15


MONITOR_INTERVAL_SECONDS = 60








async def monitor_operators(


    bot: Bot,


    session_factory: async_sessionmaker,


) -> None:


    async with session_factory() as session:


        dao = OperatorShiftDAO(session)





        stale_shifts = await dao.get_stale_shifts(


            inactive_after_minutes=INACTIVE_AFTER_MINUTES,


        )





        for shift in stale_shifts:


            await dao.stop_shift(shift.id)





            try:


                await bot.send_message(


                    shift.operator_id,


                    "⏱ Смена закрыта автоматически из-за неактивности",


                )


            except Exception as e:


                logger.warning(


                    "Failed to notify operator %s: %s",


                    shift.operator_id,


                    e,


                )





        await session.commit()








async def operator_monitor_loop(


    bot: Bot,


    session_factory: async_sessionmaker,


) -> None:


    while True:


        try:


            await monitor_operators(bot, session_factory)


        except Exception:


            logger.exception("❌ Operator monitor crashed")





        await asyncio.sleep(MONITOR_INTERVAL_SECONDS)






