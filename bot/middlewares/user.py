# bot/middlewares/user.py
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.dao.users_dao import UsersDAO


class EnsureUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict], Awaitable[Any]],
        event: Update,
        data: dict,
    ) -> Any:
        user = self._extract_user(event)
        if not user:
            # системный апдейт — просто пропускаем
            return await handler(event, data)

        session = data["session"]
        users = UsersDAO(session)

        db_user = await users.get_or_create(
            tg_id=user.id
        )

        data["user"] = db_user
        return await handler(event, data)

    @staticmethod
    def _extract_user(event: Update):
        if event.message and event.message.from_user:
            return event.message.from_user

        if event.callback_query and event.callback_query.from_user:
            return event.callback_query.from_user

        if event.inline_query and event.inline_query.from_user:
            return event.inline_query.from_user

        if event.chat_member and event.chat_member.from_user:
            return event.chat_member.from_user

        return None
