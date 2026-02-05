from pathlib import Path

MODELS_DIR = Path("bot/models")

TYPE_CHECK_BLOCK = """from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order_item import OrderItem
    from .user import User
    from .payment import Payment
"""

for file in MODELS_DIR.glob("*.py"):
    text = file.read_text(encoding="utf-8")

    if "TYPE_CHECKING" in text:
        continue

    lines = text.splitlines()

    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("from") or line.startswith("import"):
            insert_at = i + 1

    lines.insert(insert_at, "")
    lines.insert(insert_at + 1, TYPE_CHECK_BLOCK.rstrip())

    file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[FIXED] {file}")

print("✅ TYPE_CHECKING added to models")
