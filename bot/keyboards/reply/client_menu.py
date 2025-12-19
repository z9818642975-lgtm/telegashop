from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def client_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Каталог"), KeyboardButton(text="🧺 Корзина")],
            [KeyboardButton(text="💬 Связь с оператором")]
        ],
        resize_keyboard=True
    )
