from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.operator_shift import OperatorShift


class OperatorShiftStateError(Exception):
    """
    Р С›РЎв‚¬Р С‘Р В±Р С”Р В° Р Р…Р ВµР С”Р С•РЎР‚РЎР‚Р ВµР С”РЎвЂљР Р…Р С•Р С–Р С• РЎРѓР С•РЎРѓРЎвЂљР С•РЎРЏР Р…Р С‘РЎРЏ РЎРѓР СР ВµР Р…РЎвЂ№
    (Р Р…Р В°Р С—РЎР‚Р С‘Р СР ВµРЎР‚, Р С—Р С•Р С—РЎвЂ№РЎвЂљР С”Р В° Р С•РЎвЂљР С”РЎР‚РЎвЂ№РЎвЂљРЎРЉ Р Р†РЎвЂљР С•РЎР‚РЎС“РЎР‹ РЎРѓР СР ВµР Р…РЎС“).
    """
    pass


class OperatorShiftDAO:
    """
    DAO Р Т‘Р В»РЎРЏ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎРѓР С”Р С‘РЎвЂ¦ РЎРѓР СР ВµР Р….

    Р С™Р С’Р СњР С›Р Сњ Р СљР С›Р вЂќР вЂўР вЂєР В (Р В·Р В°РЎвЂћР С‘Р С”РЎРѓР С‘РЎР‚Р С•Р Р†Р В°Р Р…Р С•):
    --------------------------------
    - Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ = Р В°Р С”РЎвЂљР С‘Р Р†Р Р…Р В°РЎРЏ OperatorShift
    - РЎРѓР С”Р В»Р В°Р Т‘ Р С”Р В°Р С” РЎРѓРЎС“РЎвЂ°Р Р…Р С•РЎРѓРЎвЂљРЎРЉ Р СњР вЂў Р С‘РЎРѓР С—Р С•Р В»РЎРЉР В·РЎС“Р ВµРЎвЂљРЎРѓРЎРЏ
    - Р Р†РЎРѓР Вµ Р С—РЎР‚Р С•Р Р†Р ВµРЎР‚Р С”Р С‘ Р Т‘Р С•РЎРѓРЎвЂљРЎС“Р С—Р В° Р С‘ SLA Р С‘Р Т‘РЎС“РЎвЂљ РЎвЂЎР ВµРЎР‚Р ВµР В· РЎРѓР СР ВµР Р…РЎС“
    """

    WARN_15 = 15
    WARN_17 = 17
    AUTO_CLOSE = 20

    def __init__(self, session: AsyncSession):
        self.session = session

    # ============================================================
    # ACTIVE
    # ============================================================

    async def get_active(self, operator_id: int) -> OperatorShift | None:
        """
        Р вЂ™Р С•Р В·Р Р†РЎР‚Р В°РЎвЂ°Р В°Р ВµРЎвЂљ Р В°Р С”РЎвЂљР С‘Р Р†Р Р…РЎС“РЎР‹ РЎРѓР СР ВµР Р…РЎС“ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В° Р С‘Р В»Р С‘ None.
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
        Р вЂ™Р С•Р В·Р Р†РЎР‚Р В°РЎвЂ°Р В°Р ВµРЎвЂљ Р вЂ™Р РЋР вЂў Р В°Р С”РЎвЂљР С‘Р Р†Р Р…РЎвЂ№Р Вµ РЎРѓР СР ВµР Р…РЎвЂ№ (Р Т‘Р В»РЎРЏ РЎРѓРЎвЂљР В°РЎР‚РЎвЂљР В° / Р С•Р Р…Р В»Р В°Р в„–Р Р…Р В°).
        """
        res = await self.session.execute(
            select(OperatorShift)
            .where(OperatorShift.ended_at.is_(None))
            .order_by(OperatorShift.started_at)
        )
        return list(res.scalars().all())

    async def is_on_shift(self, operator_id: int) -> bool:
        """
        Р СџРЎР‚Р С•Р Р†Р ВµРЎР‚Р С”Р В°: Р ВµРЎРѓРЎвЂљРЎРЉ Р В»Р С‘ РЎС“ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В° Р В°Р С”РЎвЂљР С‘Р Р†Р Р…Р В°РЎРЏ РЎРѓР СР ВµР Р…Р В°.
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
        Р С›РЎвЂљР С”РЎР‚РЎвЂ№РЎвЂљР С‘Р Вµ РЎРѓР СР ВµР Р…РЎвЂ№.
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
        Р вЂ”Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР С‘Р Вµ Р В°Р С”РЎвЂљР С‘Р Р†Р Р…Р С•Р в„– РЎРѓР СР ВµР Р…РЎвЂ№ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°.
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
        Р вЂ”Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР С‘Р Вµ РЎРѓР СР ВµР Р…РЎвЂ№ Р С—Р С• ID (Р С‘РЎРѓР С—Р С•Р В»РЎРЉР В·РЎС“Р ВµРЎвЂљРЎРѓРЎРЏ watcher'Р С•Р С).
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
        Р С›Р В±Р Р…Р С•Р Р†Р В»Р ВµР Р…Р С‘Р Вµ Р В°Р С”РЎвЂљР С‘Р Р†Р Р…Р С•РЎРѓРЎвЂљР С‘ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°.
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
        Р вЂ™Р С•Р В·Р Р†РЎР‚Р В°РЎвЂ°Р В°Р ВµРЎвЂљ РЎРѓР СР ВµР Р…РЎвЂ№ Р В±Р ВµР В· Р В°Р С”РЎвЂљР С‘Р Р†Р Р…Р С•РЎРѓРЎвЂљР С‘ Р Т‘Р С•Р В»РЎРЉРЎв‚¬Р Вµ inactive_minutes.
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
        Р СџР С•Р СР ВµРЎвЂЎР В°Р ВµРЎвЂљ РЎРѓР СР ВµР Р…РЎС“ Р С”Р В°Р С” Р С—РЎР‚Р ВµР Т‘РЎС“Р С—РЎР‚Р ВµР В¶Р Т‘РЎвЂР Р…Р Р…РЎС“РЎР‹
        (15 / 17 / 20 Р СР С‘Р Р…РЎС“РЎвЂљ).
        """
        if minutes == self.WARN_15:
            field = OperatorShift.warned_15
        elif minutes == self.WARN_17:
            field = OperatorShift.warned_17
        elif minutes == self.AUTO_CLOSE:
            field = OperatorShift.warned_20
        else:
            raise ValueError("Unsupported warning interval")

        await self.session.execute(
            update(OperatorShift)
            .where(OperatorShift.id == shift_id)
            .values({field: True})
        )

    # ============================================================
    # PICKUP INFO
    # ============================================================

    async def update_pickup_info(
        self,
        *,
        operator_id: int,
        description: str | None = None,
        photos: list[str] | None = None,
    ):
        values = {}
        if description is not None:
            values["pickup_description"] = description
        if photos is not None:
            values["pickup_photos"] = photos

        if not values:
            return

        await self.session.execute(
            update(OperatorShift)
            .where(
                OperatorShift.operator_id == operator_id,
                OperatorShift.ended_at.is_(None),
            )
            .values(**values)
        )

