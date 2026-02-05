# bot/constants/callbacks_demo.py
from aiogram.filters.callback_data import CallbackData


class DemoCB(CallbackData, prefix="demo"):
    action: str
