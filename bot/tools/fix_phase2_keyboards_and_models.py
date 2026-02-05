import re
from pathlib import Path

# =========================
# 1. ADMIN KEYBOARDS — ADD MISSING CALLBACK IMPORTS
# =========================

ADMIN_FIXES = {
    "salary.py": [
        "from bot.constants.callbacks_admin import AdminSalaryPayCB",
    ],
    "stocks.py": [
        "from bot.constants.callbacks_admin import AdminWarehousesStockCB, AdminWarehouseSelectCB",
    ],
    "warehouses.py": [
        "from bot.constants.callbacks_admin import AdminWarehouseSelectCB",
        "from bot.constants.callbacks_common import BackCB",
    ],
}

ADMIN_DIR = Path("bot/keyboards/admin")

for file in ADMIN_DIR.glob("*.py"):
    if file.name not in ADMIN_FIXES:
        continue

    text = file.read_text(encoding="utf-8")
    imports = ADMIN_FIXES[file.name]

    for imp in imports:
        if imp not in text:
            text = imp + "\n" + text

    file.write_text(text, encoding="utf-8")
    print(f"[ADMIN FIX] {file}")


# =========================
# 2. FIX BROKEN warehouse_actions.py
# =========================

WA = ADMIN_DIR / "warehouse_actions.py"
if WA.exists():
    WA.write_text(
        """from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import (
    AdminWarehouseDeactivateCB,
    AdminWarehouseMoveCB,
    AdminWarehouseProductsCB,
    AdminWarehousesListCB,
)


def admin_warehouse_actions_kb(warehouse_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📦 Товары на складе",
                callback_data=AdminWarehouseProductsCB(
                    warehouse_id=warehouse_id
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🔁 Переместить товары",
                callback_data=AdminWarehouseMoveCB(
                    warehouse_id=warehouse_id
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🛑 Архивировать склад",
                callback_data=AdminWarehouseDeactivateCB(
                    warehouse_id=warehouse_id
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ К складам",
                callback_data=AdminWarehousesListCB().pack(),
            )
        ],
    ])
""",
        encoding="utf-8",
    )
    print("[ADMIN FIX] warehouse_actions.py rewritten")


# =========================
# 3. REMOVE F811 DUPLICATES (client / operator)
# =========================

BAD_IMPORT_RE = re.compile(
    r"from bot\.constants\.callbacks_common import .*"
)

KEYBOARD_DIRS = [
    Path("bot/keyboards/client"),
    Path("bot/keyboards/operator"),
]

for d in KEYBOARD_DIRS:
    for file in d.glob("*.py"):
        text = file.read_text(encoding="utf-8")
        new_lines = [
            line for line in text.splitlines()
            if not BAD_IMPORT_RE.match(line)
        ]
        new_text = "\n".join(new_lines)

        if new_text != text:
            file.write_text(new_text, encoding="utf-8")
            print(f"[DEDUP] {file}")


# =========================
# 4. MODELS — ADD MISSING TYPE_CHECKING IMPORTS
# =========================

MODELS = {
    "payment.py": [
        "from .order import Order",
        "from .bank_account import BankAccount",
    ],
    "user.py": [
        "from .order import Order",
    ],
}

MODELS_DIR = Path("bot/models")

for name, imports in MODELS.items():
    file = MODELS_DIR / name
    if not file.exists():
        continue

    text = file.read_text(encoding="utf-8")
    if "TYPE_CHECKING" not in text:
        continue

    for imp in imports:
        if imp not in text:
            text = text.replace(
                "if TYPE_CHECKING:",
                "if TYPE_CHECKING:\n    " + imp,
                1,
            )

    file.write_text(text, encoding="utf-8")
    print(f"[MODEL FIX] {file}")

print("✅ PHASE 2 FIX COMPLETE")
