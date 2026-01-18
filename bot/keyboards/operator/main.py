from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def operator_main_menu(*, on_shift: bool) -> ReplyKeyboardMarkup:
    """
    Главное меню оператора.
    Контракт:
    - on_shift=True  → кнопки работы
    - on_shift=False → только вход на смену
    """

    if not on_shift:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🟢 Выйти на смену")],
                [KeyboardButton(text="⬅️ Назад")],
            ],
            resize_keyboard=True,
        )

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Заказы")],
            [KeyboardButton(text="⏸ Закрыть смену")],
        ],
        resize_keyboard=True,
    )

