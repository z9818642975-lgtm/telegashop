# bot/keyboards/client/pickup.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import ClientCartOpen


def client_pickup_addresses_kb(shifts):
    rows = []
    for s in shifts:
        rows.append([
            InlineKeyboardButton(
                text=s.pickup_address,
callback_data=ClientCartOpen().pack()
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)

