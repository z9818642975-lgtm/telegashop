from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOT = ROOT / "bot"
SELF = Path(__file__).resolve()

# =========================
# 1. REMOVE POWERSHELL .py
# =========================
for p in BOT.rglob("*.py"):
    # 🔒 никогда не трогаем сам скрипт
    if p.resolve() == SELF:
        continue

    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue

    # чёткий PowerShell-сигнатурный детект
    if (
        text.lstrip().startswith("$ErrorActionPreference")
        or re.search(r"\bfunction\s+\w+-\w+", text)
    ):
        new = p.with_suffix(".ps1")
        print(f"[REMOVE] {p} → {new}")
        p.rename(new)

# =========================
# 2. FIX Base redefinition
# =========================
init_db = BOT / "bootstrap" / "init_db.py"
if init_db.exists():
    text = init_db.read_text(encoding="utf-8")
    text = re.sub(
        r"from bot\.db import Base,\s*async_session_maker,\s*engine\s*\n",
        "from bot.db import async_session_maker, engine\n",
        text,
    )
    init_db.write_text(text, encoding="utf-8")

# =========================
# 3. SAFE REWRITES
# =========================
for file in BOT.rglob("*.py"):
    if "tools" in file.parts:
        continue

    try:
        text = file.read_text(encoding="utf-8")
    except Exception:
        continue

    original = text

    text = text.replace("F.data == None", "F.data.is_(None)")
    text = re.sub(r";\s*await", "\n    await", text)
    text = re.sub(r"\bfor l in ", "for log in ", text)

    if text != original:
        file.write_text(text, encoding="utf-8")

# =========================
# 4. ADD MISSING IMPORTS
# =========================
IMPORTS = {
    "F": "from aiogram import F",
    "Command": "from aiogram.filters import Command",
    "InlineKeyboardButton": "from aiogram.types import InlineKeyboardButton",
    "InlineKeyboardMarkup": "from aiogram.types import InlineKeyboardMarkup",
}

for file in BOT.rglob("*.py"):
    try:
        text = file.read_text(encoding="utf-8")
    except Exception:
        continue

    needed = []
    for symbol, imp in IMPORTS.items():
        if symbol in text and imp not in text:
            needed.append(imp)

    if needed:
        lines = text.splitlines()
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("import") or line.startswith("from"):
                insert_at = i + 1

        for imp in needed:
            lines.insert(insert_at, imp)
            insert_at += 1

        file.write_text("\n".join(lines), encoding="utf-8")

# =========================
# 5. FUTURE ANNOTATIONS
# =========================
models_dir = BOT / "models"
for file in models_dir.rglob("*.py"):
    try:
        text = file.read_text(encoding="utf-8")
    except Exception:
        continue

    if "from __future__ import annotations" not in text:
        file.write_text(
            "from __future__ import annotations\n\n" + text,
            encoding="utf-8",
        )

print("\n✅ AUTO-FIX COMPLETE (SAFE MODE)")
