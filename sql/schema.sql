class UsersDAO:
    def __init__(self, session):
        self.session = session

    async def get_by_tg_id(self, tg_id: int):
        result = await self.session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one_or_none()

