from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def operator_main_menu_kb(on_shift: bool) -> ReplyKeyboardMarkup:
    if not on_shift:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🟢 Начать смену")],
            ],
            resize_keyboard=True,
        )

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Активные заказы")],
            [KeyboardButton(text="🔴 Завершить смену")],
        ],
        resize_keyboard=True,
    )