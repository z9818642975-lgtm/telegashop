from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏬 Склады",
                    callback_data="admin:warehouses",
                ),
                InlineKeyboardButton(
                    text="📦 Товары",
                    callback_data="admin:products",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="👷 Операторы",
                    callback_data="admin:operators",
                ),
                InlineKeyboardButton(
                    text="🏦 Банки",
                    callback_data="admin:banks",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📊 Статистика",
                    callback_data="admin:stats",
                ),
            ],
        ]
    )

