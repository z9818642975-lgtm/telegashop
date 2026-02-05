# bot/dao/operator_shift_dao.py
from datetime import datetime, timedelta

from sqlalchemy import select, update

from bot.dao.base import BaseDAO
from bot.models.operator_shift import OperatorShift


class OperatorShiftDAO(BaseDAO):
    WARN_15_MINUTES = 15
    WARN_17_MINUTES = 17
    AUTO_CLOSE_MINUTES = 20

    # ────────────────
    # BASIC OPERATIONS
    # ────────────────

    async def get_active(self, operator_id: int) -> OperatorShift | None:
        res = await self.session.execute(
            select(OperatorShift).where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.ended_at.is_(None),
            )
        )
        return res.scalar_one_or_none()

    async def start(self, operator_id: int, pickup_address: str) -> OperatorShift:
        shift = OperatorShift(
            operator_id=operator_id,
            pickup_address=pickup_address,
            started_at=datetime.utcnow(),
        )
        self.session.add(shift)
        await self.session.flush()
        return shift

    async def stop(self, operator_id: int):
        await self.session.execute(
            update(OperatorShift)
            .where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.ended_at.is_(None),
            )
            .values(ended_at=datetime.utcnow())
        )

    async def stop_by_id(self, shift_id: int, auto: bool = False):
        await self.session.execute(
            update(OperatorShift)
            .where(OperatorShift.id == shift_id)
            .values(
                ended_at=datetime.utcnow(),
                auto_closed=auto,
            )
        )

    # ─────────────────────────
    # WATCHER-SPECIFIC METHODS
    # ─────────────────────────

    async def get_active_older_than(self, minutes: int) -> list[OperatorShift]:
        """
        Активные смены, которые длятся дольше N минут
        """
        border = datetime.utcnow() - timedelta(minutes=minutes)

        res = await self.session.execute(
            select(OperatorShift).where(
                OperatorShift.ended_at.is_(None),
                OperatorShift.started_at <= border,
            )
        )
        return res.scalars().all()

    async def mark_warned(self, shift_id: int, level: int):
        field = {
            15: OperatorShift.warned_15,
            17: OperatorShift.warned_17,
            20: OperatorShift.warned_20,
        }.get(level)

        if not field:
            return

        await self.session.execute(
            update(OperatorShift)
            .where(OperatorShift.id == shift_id)
            .values({field: True})
        )
