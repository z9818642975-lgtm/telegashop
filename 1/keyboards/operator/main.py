from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def operator_main_menu(*, on_shift: bool) -> ReplyKeyboardMarkup:
    """
    Р вЂњР В»Р В°Р Р†Р Р…Р С•Р Вµ Р СР ВµР Р…РЎР‹ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°.
    Р С™Р С•Р Р…РЎвЂљРЎР‚Р В°Р С”РЎвЂљ:
    - on_shift=True  РІвЂ вЂ™ Р С”Р Р…Р С•Р С—Р С”Р С‘ РЎР‚Р В°Р В±Р С•РЎвЂљРЎвЂ№
    - on_shift=False РІвЂ вЂ™ РЎвЂљР С•Р В»РЎРЉР С”Р С• Р Р†РЎвЂ¦Р С•Р Т‘ Р Р…Р В° РЎРѓР СР ВµР Р…РЎС“
    """

    if not on_shift:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="СЂСџСџСћ Р вЂ™РЎвЂ№Р в„–РЎвЂљР С‘ Р Р…Р В° РЎРѓР СР ВµР Р…РЎС“")],
                [KeyboardButton(text="РІВ¬вЂ¦РїС‘РЏ Р СњР В°Р В·Р В°Р Т‘")],
            ],
            resize_keyboard=True,
        )

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="СЂСџвЂњВ¦ Р вЂ”Р В°Р С”Р В°Р В·РЎвЂ№")],
            [KeyboardButton(text="РІРЏС‘ Р вЂ”Р В°Р С”РЎР‚РЎвЂ№РЎвЂљРЎРЉ РЎРѓР СР ВµР Р…РЎС“")],
        ],
        resize_keyboard=True,
    )

