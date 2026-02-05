# bot/keyboards/client/pickup_actions.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import ClientPaymentDone
from bot.constants.callbacks_common import ClientPaymentCancel


def client_pickup_actions_kb(order_item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⏱ 10 минут",
                callback_data=ClientPaymentCancel().pack(),
            ),
            InlineKeyboardButton(
                text="✅ Забрал",
                callback_data=ClientPaymentDone().pack(),
            ),
        ]
    ])