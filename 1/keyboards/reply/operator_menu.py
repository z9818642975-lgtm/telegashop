from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def operator_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="рџ“¦ Р—Р°РєР°Р·С‹")],
            [KeyboardButton(text="вЏ± РћС‚РєСЂС‹С‚СЊ СЃРјРµРЅСѓ")],
            [KeyboardButton(text="вќЊ Р—Р°РєСЂС‹С‚СЊ СЃРјРµРЅСѓ")],
        ],
        resize_keyboard=True,
    )

