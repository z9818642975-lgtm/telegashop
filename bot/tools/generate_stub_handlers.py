import re
from pathlib import Path

CALLBACK_RE = re.compile(r"callback_data=([A-Za-z0-9_]+)\(")

KEYBOARD_DIRS = [
    Path("bot/keyboards/client"),
    Path("bot/keyboards/operator"),
    Path("bot/keyboards/admin"),
]

found = set()

for d in KEYBOARD_DIRS:
    for file in d.glob("*.py"):
        text = file.read_text(encoding="utf-8")
        for m in CALLBACK_RE.findall(text):
            found.add(m)

OUT = Path("bot/routers/stub_handlers.py")

lines = [
    "from aiogram import Router",
    "from aiogram.types import CallbackQuery",
    "from sqlalchemy.ext.asyncio import AsyncSession",
    "",
    "router = Router(name='stub_handlers')",
    "",
]

for cb in sorted(found):
    lines.extend([
        f"@router.callback_query({cb}.filter())",
        f"async def stub_{cb.lower()}(",
        "    cb: CallbackQuery,",
        f"    callback_data: {cb},",
        "    session: AsyncSession,",
        "):",
        "    await cb.answer('⏳ В разработке')",
        "",
    ])

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"✅ Stub handlers generated: {OUT}")
