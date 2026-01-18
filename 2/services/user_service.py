# -*- coding: utf-8 -*-
# bot/services/user_service.py
# bot/services/user_service.py


from __future__ import annotations





from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import select





from bot.models.user import User








class UserService:


    def __init__(self, session: AsyncSession):


        self.session = session





    async def get_or_create(


        self,


        tg_id: int,


        username: str | None = None,


    ) -> User:


        result = await self.session.execute(


            select(User).where(User.tg_id == tg_id)


        )


        user = result.scalars().first()





        if user:


            return user





        user = User(


            tg_id=tg_id,


            username=username,


            role="client",  # 👈 по умолчанию


        )


        self.session.add(user)


        await self.session.flush()


        return user





