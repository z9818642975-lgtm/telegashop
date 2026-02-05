# bot/keyboards/admin/main.py
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def admin_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="А 📦 Товары"),
                KeyboardButton(text="А 🏦 Банки"),
            ],
            [
                KeyboardButton(text="А 👷 Операторы"),
                KeyboardButton(text="А 🏬 Склады"),
            ],
            [
                KeyboardButton(text="А 📋 Заказы"),
                KeyboardButton(text="А 💰 Зарплаты"),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )