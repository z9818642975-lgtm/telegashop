from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models.user import User


def operators_kb(operators: list[User]) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []

    for op in operators:
        status = "Р РЋР вЂљР РЋРЎСџР РЋРЎСџР РЋРЎвЂє" if op.is_active else "Р В Р вЂ Р РЋРІвЂћСћР вЂ™Р’В«Р В РЎвЂ”Р РЋРІР‚ВР В Р РЏ"
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
                text="Р В Р вЂ Р вЂ™Р’В¬Р Р†Р вЂљР’В¦Р В РЎвЂ”Р РЋРІР‚ВР В Р РЏ Р В Р’В Р РЋРЎС™Р В Р’В Р вЂ™Р’В°Р В Р’В Р вЂ™Р’В·Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚В",
                callback_data="admin:panel",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

