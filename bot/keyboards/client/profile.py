from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def profile_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Мои заказы",
                    callback_data="profile:orders",
                ),
                InlineKeyboardButton(
                    text="👥 Рефералы",
                    callback_data="profile:ref",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎟 Купон",
                    callback_data="profile:coupon",
                ),
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=CB.BACK_MENU,
                ),
            ],
        ]
    )

