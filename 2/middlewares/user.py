# bot/middlewares/user.py

# bot/middlewares/user.py
# bot/middlewares/user.py


from aiogram import BaseMiddleware


from aiogram.types import Update


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.users_dao import UsersDAO








class EnsureUserMiddleware(BaseMiddleware):


    async def __call__(self, handler, event: Update, data: dict):


        session: AsyncSession | None = data.get("session")


        if session is None:


            return await handler(event, data)





        tg_user = None


        if event.message:


            tg_user = event.message.from_user


        elif event.callback_query:


            tg_user = event.callback_query.from_user





        if tg_user is None:


            return await handler(event, data)





        users = UsersDAO(session)


        user = await users.get_or_create(tg_user)





        data["user"] = user


        return await handler(event, data)




