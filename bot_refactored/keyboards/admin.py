from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👷 Операторы", callback_data="admin:operators")],
        [InlineKeyboardButton(text="💬 Чаты", callback_data="admin:chats")],
    ])

def operators_kb(operators, page: int, pages: int):
    kb = []
    for op in operators:
        kb.append([
            InlineKeyboardButton(
                text=f"👷 {op.telegram_id} ({'ON' if op.is_active else 'OFF'})",
                callback_data=f"admin:operator:{op.telegram_id}"
            )
        ])
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"admin:operators:{page-1}"))
    if page < pages:
        nav.append(InlineKeyboardButton("➡️", callback_data=f"admin:operators:{page+1}"))
    if nav:
        kb.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=kb)

