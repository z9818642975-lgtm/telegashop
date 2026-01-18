from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class UserMiddleware(BaseMiddleware):
    """
    РџСЂРѕРєРёРґС‹РІР°РµС‚ `user` РІ handler kwargs,
    С‡С‚РѕР±С‹ legacy-С…РµРЅРґР»РµСЂС‹ СЃ Р°СЂРіСѓРјРµРЅС‚РѕРј `user` СЂР°Р±РѕС‚Р°Р»Рё.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if "user" not in data:
            tg_user = getattr(event, "from_user", None)
            if tg_user is not None:
                data["user"] = tg_user

        return await handler(event, data)

