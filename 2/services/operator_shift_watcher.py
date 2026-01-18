# bot/services/operator_shift_watcher.py
from __future__ import annotations

import asyncio
from datetime import datetime

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import ProgrammingError

from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.keyboards.operator.heartbeat import iam_here_kb


CHECK_INTERVAL = 60  # секунд


async def operator_shift_watcher(
    *,
    bot: Bot,
    sessionmaker: async_sessionmaker,
):
    """
    Глобальный watchdog операторских смен.

    Тайминги:
      - 15 мин → предупреждение
      - 17 мин → финальное предупреждение
      - 20 мин → автозакрытие
    """

    while True:
        try:
            async with sessionmaker() as session:
                dao = OperatorShiftDAO(session)
                now = datetime.utcnow()

                # ============================================================
                # 20 минут — АВТОЗАКРЫТИЕ (СНАЧАЛА!)
                # ============================================================

                shifts_20 = await dao.get_stale_shifts(
                    inactive_minutes=dao.AUTO_CLOSE
                )
                for shift in shifts_20:
                    if shift.warned_20:
                        continue

                    await bot.send_message(
                        shift.operator_id,
                        "❌ Смена автоматически закрыта из-за неактивности.",
                    )

                    # сначала помечаем, потом закрываем — защита от гонок
                    await dao.mark_warned(
                        shift_id=shift.id,
                        minutes=dao.AUTO_CLOSE,
                    )
                    await dao.stop_shift_by_id(shift_id=shift.id)

                # ============================================================
                # 17 минут — ФИНАЛЬНОЕ ПРЕДУПРЕЖДЕНИЕ
                # ============================================================

                shifts_17 = await dao.get_stale_shifts(
                    inactive_minutes=dao.WARN_17
                )
                for shift in shifts_17:
                    if shift.warned_17 or shift.warned_20:
                        continue

                    await bot.send_message(
                        shift.operator_id,
                        "⏰ Последнее предупреждение.\n"
                        "Через 3 минуты смена будет закрыта.",
                        reply_markup=iam_here_kb(),
                    )
                    await dao.mark_warned(
                        shift_id=shift.id,
                        minutes=dao.WARN_17,
                    )

                # ============================================================
                # 15 минут — ПЕРВОЕ ПРЕДУПРЕЖДЕНИЕ
                # ============================================================

                shifts_15 = await dao.get_stale_shifts(
                    inactive_minutes=dao.WARN_15
                )
                for shift in shifts_15:
                    if shift.warned_15 or shift.warned_17 or shift.warned_20:
                        continue

                    await bot.send_message(
                        shift.operator_id,
                        "⚠️ Вы неактивны 15 минут.\n"
                        "Нажмите «Я на месте».",
                        reply_markup=iam_here_kb(),
                    )
                    await dao.mark_warned(
                        shift_id=shift.id,
                        minutes=dao.WARN_15,
                    )

                await session.commit()

        except ProgrammingError:
            # БД ещё не готова или миграция в процессе
            pass
        except Exception:
            # watcher не должен умирать ни при каких условиях
            pass

        await asyncio.sleep(CHECK_INTERVAL)

