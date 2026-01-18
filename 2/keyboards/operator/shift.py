from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB

on_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🚀 Выйти на смену", callback_data=CB.OP_SHIFT_START)]
    ]
)

off_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("⛔ Завершить смену", callback_data=CB.OP_SHIFT_STOP)],
        [InlineKeyboardButton("✏️ Изменить адрес", callback_data=CB.OP_SHIFT_EDIT_ADDRESS)],
    ]
)

confirm_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("✅ Подтвердить", callback_data=CB.OP_SHIFT_CONFIRM)],
        [InlineKeyboardButton("❌ Отмена", callback_data=CB.OP_SHIFT_CANCEL)],
    ]
)

