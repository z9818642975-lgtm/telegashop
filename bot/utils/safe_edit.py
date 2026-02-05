# bot/utils/safe_edit.py
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup


async def safe_edit_text(
    message,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    **kwargs,
):
    """
    Универсальный safe edit_text.

    Допускает:
    - positional text
    - keyword text
    - parse_mode, disable_web_page_preview и т.д.

    Никогда не падает на 'message is not modified'
    """
    try:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            **kwargs,
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        raise


