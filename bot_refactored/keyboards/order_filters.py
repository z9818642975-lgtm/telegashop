from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_refactored.models.order import OrderStatus


def order_filter_kb(prefix: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("🆕 NEW", callback_data=f"{prefix}:status:{OrderStatus.NEW}"),
            InlineKeyboardButton("✅ ACCEPTED", callback_data=f"{prefix}:status:{OrderStatus.ACCEPTED}"),
        ],
        [
            InlineKeyboardButton("⏳ WAIT", callback_data=f"{prefix}:status:{OrderStatus.WAITING_CONFIRMATION}"),
            InlineKeyboardButton("💰 PAID", callback_data=f"{prefix}:status:{OrderStatus.PAID}"),
        ],
        [
            InlineKeyboardButton("✔ DONE", callback_data=f"{prefix}:status:{OrderStatus.DONE}"),
        ],
    ])

