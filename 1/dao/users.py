from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.user import User


class UsersDAO:
    @staticmethod
    async def get_or_create(session: AsyncSession, tg_id: int) -> User:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()
        if user:
            return user

        user = User(tg_id=tg_id)
        session.add(user)
        await session.flush()
        return user

