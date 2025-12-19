from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.user import User

class UsersDAO:
    def __init__(self, s: AsyncSession): self.s = s

    async def get_or_create(self, tg_id: int, **data) -> User:
        res = await self.s.execute(select(User).where(User.tg_id == tg_id))
        u = res.scalar_one_or_none()
        if u: return u
        u = User(tg_id=tg_id, **data)
        self.s.add(u); await self.s.flush()
        return u

    async def get_by_tg(self, tg_id: int) -> User | None:
        res = await self.s.execute(select(User).where(User.tg_id == tg_id))
        return res.scalar_one_or_none()

    async def list_operators_with_active_shift(self):
        res = await self.s.execute(select(User).where(User.role == "OPERATOR", User.is_active.is_(True)))
        return res.scalars().all()
