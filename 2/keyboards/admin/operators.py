from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models.user import User


def operators_kb(operators: list[User]) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []

    for op in operators:
        status = "🟢" if op.is_active else "⚫️"
        name = op.full_name or op.username or f"ID {op.id}"

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{status} {name}",
                    callback_data=f"admin:operator:toggle:{op.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="admin:panel",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

