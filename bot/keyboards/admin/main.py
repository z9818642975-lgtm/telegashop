# bot/keyboards/admin/main.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📦 Товары"),
                KeyboardButton(text="🏦 Банки"),
            ],
            [
                KeyboardButton(text="👷 Операторы"),
                KeyboardButton(text="🏬 Склады"),
            ],
            [
                KeyboardButton(text="📊 Статистика"),
            ],
        ],
        resize_keyboard=True,
        selective=True,
    )

