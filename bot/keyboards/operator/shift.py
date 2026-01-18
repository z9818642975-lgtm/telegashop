from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB

on_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Выйти на смену", callback_data=CB.OP_SHIFT_START)]
    ]
)

off_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⛔ Завершить смену", callback_data=CB.OP_SHIFT_STOP)],
        [InlineKeyboardButton(text="✏️ Изменить адрес", callback_data=CB.OP_SHIFT_EDIT_ADDRESS)],
    ]
)

confirm_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=CB.OP_SHIFT_CONFIRM)],
        [InlineKeyboardButton(text="❌ Отмена", callback_data=CB.OP_SHIFT_CANCEL)],
    ]
)

