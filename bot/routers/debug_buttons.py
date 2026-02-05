from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

router = Router(name="debug_buttons")


def debug_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧪 Кнопка A",
                    callback_data="DEBUG:A"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧪 Кнопка B",
                    callback_data="DEBUG:B"
                )
            ],
        ]
    )


@router.message(Command("debug"))
async def debug_start(message: Message):
    await message.answer(
        "DEBUG MODE\nНажми кнопку:",
        reply_markup=debug_kb()
    )


@router.callback_query(lambda c: c.data.startswith("DEBUG:"))
async def debug_click(cb: CallbackQuery):
    await cb.answer(f"Нажата {cb.data}")
    await cb.message.answer(f"OK: {cb.data}")