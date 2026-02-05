# bot/routers/common/guards.py
from aiogram.types import TelegramObject


def client_guard(event: TelegramObject, data: dict) -> bool:
    user = data.get("user")
    return bool(user and user.role == "client")


def operator_guard(event: TelegramObject, data: dict) -> bool:
    user = data.get("user")
    return bool(user and user.role == "operator")


def admin_guard(event: TelegramObject, data: dict) -> bool:
    user = data.get("user")
    return bool(user and user.role == "admin")


