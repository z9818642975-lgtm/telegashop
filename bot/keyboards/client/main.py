# bot/keyboards/client/main.py
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def client_main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📦 Каталог"),
                KeyboardButton(text="🧺 Корзина"),
            ],
            [
                KeyboardButton(text="👤 Профиль"),
                KeyboardButton(text="❓ FAQ"),
            ],
            [
                KeyboardButton(text="💬 Связь с оператором"),
            ],
        ],
        resize_keyboard=True,
    )