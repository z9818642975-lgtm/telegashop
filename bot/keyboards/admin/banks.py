from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def banks_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Список банков",
                    callback_data="admin:bank:list",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="➕ Добавить банк",
                    callback_data="admin:bank:create",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="admin:panel",
                ),
            ],
        ]
    )

