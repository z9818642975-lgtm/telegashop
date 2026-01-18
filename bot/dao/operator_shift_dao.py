from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.operator_shift import OperatorShift


class OperatorShiftStateError(Exception):
    """
    Ошибка некорректного состояния смены
    (например, попытка открыть вторую смену).
    """
    pass


class OperatorShiftDAO:
    """
    DAO для операторских смен.

    КАНОН МОДЕЛИ (зафиксировано):
    --------------------------------
    - оператор = активная OperatorShift
    - склад как сущность НЕ используется
    - все проверки доступа и SLA идут через смену
    """

    # ============================================================
    # SHIFT TIMEOUTS — SOURCE OF TRUTH
    # ============================================================

    WARN_15_MINUTES = 15
    WARN_17_MINUTES = 17
    AUTO_CLOSE_MINUTES = 20

    def __init__(self, session: AsyncSession):
        self.session = session

    # ============================================================
    # ACTIVE
    # ============================================================

    async def get_active(self, operator_id: int) -> OperatorShift | None:
        """
        Возвращает активную смену оператора или None.
        """
        res = await self.session.execute(
            select(OperatorShift).where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.ended_at.is_(None),
            )
        )
        return res.scalar_one_or_none()

    async def get_active_all(self) -> list[OperatorShift]:
        """
        Возвращает ВСЕ активные смены (для watcher / онлайна).
        """
        res = await self.session.execute(
            select(OperatorShift)
            .where(OperatorShift.ended_at.is_(None))
            .order_by(OperatorShift.started_at)
        )
        return list(res.scalars().all())

    async def is_on_shift(self, operator_id: int) -> bool:
        """
        Проверка: есть ли у оператора активная смена.
        """
        return await self.get_active(operator_id) is not None

    # ============================================================
    # LIFECYCLE
    # ============================================================

    async def start_shift(
        self,
        *,
        operator_id: int,
        pickup_address: str,
    ) -> OperatorShift:
        """
        Открытие смены.
        """
        if await self.is_on_shift(operator_id):
            raise OperatorShiftStateError("Operator already on shift")

        now = datetime.utcnow()

        shift = OperatorShift(
            operator_id=operator_id,
            pickup_address=pickup_address,
            started_at=now,
            last_activity_at=now,
            warned_15=False,
            warned_17=False,
            warned_20=False,
        )

        self.session.add(shift)
        await self.session.flush()
        return shift

    async def stop_shift(self, *, operator_id: int) -> None:
        """
        Закрытие активной смены оператора.
        """
        await self.session.execute(
            update(OperatorShift)
            .where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.ended_at.is_(None),
            )
            .values(ended_at=datetime.utcnow())
        )

    async def stop_shift_by_id(self, *, shift_id: int) -> None:
        """
        Закрытие смены по ID (используется watcher'ом).
        """
        await self.session.execute(
            update(OperatorShift)
            .where(
                OperatorShift.id == shift_id,
                OperatorShift.ended_at.is_(None),
            )
            .values(ended_at=datetime.utcnow())
        )

    # ============================================================
    # HEARTBEAT
    # ============================================================

    async def touch(self, *, operator_id: int) -> None:
        """
        Обновление активности оператора.
        """
        now = datetime.utcnow()

        await self.session.execute(
            update(OperatorShift)
            .where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.ended_at.is_(None),
            )
            .values(
                last_activity_at=now,
                warned_15=False,
                warned_17=False,
                warned_20=False,
            )
        )

    # ============================================================
    # MONITORING / WATCHER
    # ============================================================

    async def get_stale_shifts(
        self,
        *,
        inactive_minutes: int,
    ) -> list[OperatorShift]:
        """
        Возвращает смены без активности дольше inactive_minutes.
        """
        cutoff = datetime.utcnow() - timedelta(minutes=inactive_minutes)

        res = await self.session.execute(
            select(OperatorShift).where(
                OperatorShift.ended_at.is_(None),
                OperatorShift.last_activity_at < cutoff,
            )
        )
        return list(res.scalars().all())

    async def mark_warned(self, *, shift_id: int, minutes: int) -> None:
        """
        Помечает смену как предупреждённую
        (15 / 17 / 20 минут).
        """
        if minutes == self.WARN_15_MINUTES:
            field = OperatorShift.warned_15
        elif minutes == self.WARN_17_MINUTES:
            field = OperatorShift.warned_17
        elif minutes == self.AUTO_CLOSE_MINUTES:
            field = OperatorShift.warned_20
        else:
            raise ValueError("Unsupported warning interval")

        await self.session.execute(
            update(OperatorShift)
            .where(OperatorShift.id == shift_id)
            .values({field: True})
        )
