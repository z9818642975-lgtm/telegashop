# bot/middlewares/role.py
from __future__ import annotations

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.models.user import User


class RoleMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        user: User | None = data.get("user")

        if user is None:
            return await handler(event, data)

        # роль уже в user (из БД)
        data["role"] = user.role

        return await handler(event, data)


