# bot/constants/action_cb.py

from aiogram.filters.callback_data import CallbackData


class ActionCB(CallbackData, prefix="act"):
    action: str
    payload: str | None = None
