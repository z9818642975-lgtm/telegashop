# bot/services/operator_shift_watcher.py
from __future__ import annotations

import asyncio
from datetime import datetime

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import ProgrammingError

from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.keyboards.operator.heartbeat import iam_here_kb


CHECK_INTERVAL = 60  # РЎРѓР ВµР С”РЎС“Р Р…Р Т‘


async def operator_shift_watcher(
    *,
    bot: Bot,
    sessionmaker: async_sessionmaker,
):
    """
    Р вЂњР В»Р С•Р В±Р В°Р В»РЎРЉР Р…РЎвЂ№Р в„– watchdog Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎРѓР С”Р С‘РЎвЂ¦ РЎРѓР СР ВµР Р….

    Р СћР В°Р в„–Р СР С‘Р Р…Р С–Р С‘:
      - 15 Р СР С‘Р Р… РІвЂ вЂ™ Р С—РЎР‚Р ВµР Т‘РЎС“Р С—РЎР‚Р ВµР В¶Р Т‘Р ВµР Р…Р С‘Р Вµ
      - 17 Р СР С‘Р Р… РІвЂ вЂ™ РЎвЂћР С‘Р Р…Р В°Р В»РЎРЉР Р…Р С•Р Вµ Р С—РЎР‚Р ВµР Т‘РЎС“Р С—РЎР‚Р ВµР В¶Р Т‘Р ВµР Р…Р С‘Р Вµ
      - 20 Р СР С‘Р Р… РІвЂ вЂ™ Р В°Р Р†РЎвЂљР С•Р В·Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР С‘Р Вµ
    """

    while True:
        try:
            async with sessionmaker() as session:
                dao = OperatorShiftDAO(session)
                now = datetime.utcnow()

                # ============================================================
                # 20 Р СР С‘Р Р…РЎС“РЎвЂљ РІР‚вЂќ Р С’Р вЂ™Р СћР С›Р вЂ”Р С’Р С™Р В Р В«Р СћР ВР вЂў (Р РЋР СњР С’Р В§Р С’Р вЂєР С’!)
                # ============================================================

                shifts_20 = await dao.get_stale_shifts(
                    inactive_minutes=dao.AUTO_CLOSE
                )
                for shift in shifts_20:
                    if shift.warned_20:
                        continue

                    await bot.send_message(
                        shift.operator_id,
                        "РІСњРЉ Р РЋР СР ВµР Р…Р В° Р В°Р Р†РЎвЂљР С•Р СР В°РЎвЂљР С‘РЎвЂЎР ВµРЎРѓР С”Р С‘ Р В·Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР В° Р С‘Р В·-Р В·Р В° Р Р…Р ВµР В°Р С”РЎвЂљР С‘Р Р†Р Р…Р С•РЎРѓРЎвЂљР С‘.",
                    )

                    # РЎРѓР Р…Р В°РЎвЂЎР В°Р В»Р В° Р С—Р С•Р СР ВµРЎвЂЎР В°Р ВµР С, Р С—Р С•РЎвЂљР С•Р С Р В·Р В°Р С”РЎР‚РЎвЂ№Р Р†Р В°Р ВµР С РІР‚вЂќ Р В·Р В°РЎвЂ°Р С‘РЎвЂљР В° Р С•РЎвЂљ Р С–Р С•Р Р…Р С•Р С”
                    await dao.mark_warned(
                        shift_id=shift.id,
                        minutes=dao.AUTO_CLOSE,
                    )
                    await dao.stop_shift_by_id(shift_id=shift.id)

                # ============================================================
                # 17 Р СР С‘Р Р…РЎС“РЎвЂљ РІР‚вЂќ Р В¤Р ВР СњР С’Р вЂєР В¬Р СњР С›Р вЂў Р СџР В Р вЂўР вЂќР Р€Р СџР В Р вЂўР вЂ“Р вЂќР вЂўР СњР ВР вЂў
                # ============================================================

                shifts_17 = await dao.get_stale_shifts(
                    inactive_minutes=dao.WARN_17
                )
                for shift in shifts_17:
                    if shift.warned_17 or shift.warned_20:
                        continue

                    await bot.send_message(
                        shift.operator_id,
                        "РІРЏВ° Р СџР С•РЎРѓР В»Р ВµР Т‘Р Р…Р ВµР Вµ Р С—РЎР‚Р ВµР Т‘РЎС“Р С—РЎР‚Р ВµР В¶Р Т‘Р ВµР Р…Р С‘Р Вµ.\n"
                        "Р В§Р ВµРЎР‚Р ВµР В· 3 Р СР С‘Р Р…РЎС“РЎвЂљРЎвЂ№ РЎРѓР СР ВµР Р…Р В° Р В±РЎС“Р Т‘Р ВµРЎвЂљ Р В·Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР В°.",
                        reply_markup=iam_here_kb(),
                    )
                    await dao.mark_warned(
                        shift_id=shift.id,
                        minutes=dao.WARN_17,
                    )

                # ============================================================
                # 15 Р СР С‘Р Р…РЎС“РЎвЂљ РІР‚вЂќ Р СџР вЂўР В Р вЂ™Р С›Р вЂў Р СџР В Р вЂўР вЂќР Р€Р СџР В Р вЂўР вЂ“Р вЂќР вЂўР СњР ВР вЂў
                # ============================================================

                shifts_15 = await dao.get_stale_shifts(
                    inactive_minutes=dao.WARN_15
                )
                for shift in shifts_15:
                    if shift.warned_15 or shift.warned_17 or shift.warned_20:
                        continue

                    await bot.send_message(
                        shift.operator_id,
                        "РІС™В РїС‘РЏ Р вЂ™РЎвЂ№ Р Р…Р ВµР В°Р С”РЎвЂљР С‘Р Р†Р Р…РЎвЂ№ 15 Р СР С‘Р Р…РЎС“РЎвЂљ.\n"
                        "Р СњР В°Р В¶Р СР С‘РЎвЂљР Вµ Р’В«Р Р‡ Р Р…Р В° Р СР ВµРЎРѓРЎвЂљР ВµР’В».",
                        reply_markup=iam_here_kb(),
                    )
                    await dao.mark_warned(
                        shift_id=shift.id,
                        minutes=dao.WARN_15,
                    )

                await session.commit()

        except ProgrammingError:
            # Р вЂР вЂќ Р ВµРЎвЂ°РЎвЂ Р Р…Р Вµ Р С–Р С•РЎвЂљР С•Р Р†Р В° Р С‘Р В»Р С‘ Р СР С‘Р С–РЎР‚Р В°РЎвЂ Р С‘РЎРЏ Р Р† Р С—РЎР‚Р С•РЎвЂ Р ВµРЎРѓРЎРѓР Вµ
            pass
        except Exception:
            # watcher Р Р…Р Вµ Р Т‘Р С•Р В»Р В¶Р ВµР Р… РЎС“Р СР С‘РЎР‚Р В°РЎвЂљРЎРЉ Р Р…Р С‘ Р С—РЎР‚Р С‘ Р С”Р В°Р С”Р С‘РЎвЂ¦ РЎС“РЎРѓР В»Р С•Р Р†Р С‘РЎРЏРЎвЂ¦
            pass

        await asyncio.sleep(CHECK_INTERVAL)

