from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks_reports import CB_REPORTS

def reports_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("рџ‘· РћС‚С‡С‘С‚ РїРѕ РѕРїРµСЂР°С‚РѕСЂСѓ", callback_data=CB_REPORTS.REPORTS_BY_OPERATOR)],
            [
                InlineKeyboardButton("рџ“¤ Р­РєСЃРїРѕСЂС‚ CSV", callback_data=CB_REPORTS.REPORTS_EXPORT_CSV),
                InlineKeyboardButton("рџ“„ Р­РєСЃРїРѕСЂС‚ PDF", callback_data=CB_REPORTS.REPORTS_EXPORT_PDF),
            ],
        ]
    )

