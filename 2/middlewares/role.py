# bot/middlewares/role.py
from aiogram import BaseMiddleware


class RoleMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # ⛔ НИКАКОЙ БД
        # ⛔ НИКАКИХ DAO
        # ⛔ НИКАКОГО create/get
        # user гарантирован EnsureUserMiddleware
        return await handler(event, data)

