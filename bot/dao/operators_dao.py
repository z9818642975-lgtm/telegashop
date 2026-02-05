# bot/dao/operators_dao.py
from sqlalchemy import select, update

from bot.dao.base import BaseDAO
from bot.models.operator import Operator


class OperatorsDAO(BaseDAO):

    async def get_by_tg(self, tg_id: int) -> Operator | None:
        res = await self.session.execute(
            select(Operator).where(Operator.tg_id == tg_id)
        )
        return res.scalar_one_or_none()

    async def list_active(self) -> list[Operator]:
        res = await self.session.execute(
            select(Operator)
            .where(Operator.is_active.is_(True))
            .order_by(Operator.id.asc())
        )
        return list(res.scalars())

    async def upsert(self, tg_id: int, name: str) -> Operator:
        op = await self.get_by_tg(tg_id)
        if op:
            op.name = name
            op.is_active = True
            return op

        op = Operator(tg_id=tg_id, name=name, is_active=True)
        self.session.add(op)
        await self.session.flush()
        return op

    async def set_active(self, tg_id: int, active: bool) -> None:
        await self.session.execute(
            update(Operator)
            .where(Operator.tg_id == tg_id)
            .values(is_active=active)
        )
