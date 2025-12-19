import asyncio
from datetime import datetime
from bot.core.db import async_session_maker
from bot.services.operator_online_service import OperatorOnlineService
from bot.core.logger import logger

async def run_online_task(bot):
    while True:
        try:
            async with async_session_maker() as s:
                svc = OperatorOnlineService(s)
                operators = await svc.list_active_operators()
                for op in operators:
                    await svc.check_operator(op.tg_id, bot=bot)
        except Exception as e:
            logger.exception("online task error: %s", e)
        await asyncio.sleep(60)
