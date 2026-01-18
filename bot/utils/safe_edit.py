from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup


async def safe_edit_text(
    message,
    *,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
):
    """
    Безопасный edit_text:
    - не падает на 'message is not modified'
    - используется везде вместо message.edit_text
    """
    try:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        raise
