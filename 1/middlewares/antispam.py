from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any

from bot.services.antispam import AntiSpamService

class AntiSpamMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        user = getattr(event, "from_user", None)
        if user and not AntiSpamService.check(user.id):
            return
        return await handler(event, data)

