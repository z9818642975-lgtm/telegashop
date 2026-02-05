import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

def write(path: pathlib.Path, content: str):
    path.write_text(content, encoding="utf-8")
    print(f"[FIXED] {path}")

# ============================================================
# 1. callbacks_common.py → ТОЛЬКО BackCB
# ============================================================

common_cb = ROOT / "bot/constants/callbacks_common.py"
write(
    common_cb,
    """from aiogram.filters.callback_data import CallbackData


class BackCB(CallbackData, prefix="back"):
    pass
"""
)

# ============================================================
# 2. Функция замены импорта Admin* из callbacks_common
# ============================================================

def fix_imports(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")

    # Admin* не могут быть в callbacks_common
    text = re.sub(
        r"from bot\.constants\.callbacks_common import ([^\n]+)",
        lambda m: (
            "from bot.constants.callbacks_admin import "
            + ", ".join(
                x.strip()
                for x in m.group(1).split(",")
                if x.strip().startswith("Admin")
            )
            + "\nfrom bot.constants.callbacks_common import BackCB"
            if any("Admin" in x for x in m.group(1).split(","))
            else m.group(0)
        ),
        text,
    )

    # BackToAdminOrders → BackCB
    text = text.replace("BackToAdminOrders", "BackCB")

    write(path, text)

# ============================================================
# 3. Пройти все admin/*.py
# ============================================================

for path in (ROOT / "bot/routers/admin").rglob("*.py"):
    if path.name == "statistics.py":
        continue
    fix_imports(path)

# ============================================================
# 4. Удалить wildcard-back хендлеры
# ============================================================

def remove_wildcard_back(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        r"@router\.callback_query\(RoleFilter\(\"admin\"\)\)\nasync def [\s\S]+?\n\n",
        re.MULTILINE,
    )

    new_text, n = pattern.subn("", text)
    if n:
        write(path, new_text)

for path in (ROOT / "bot/routers/admin").rglob("*.py"):
    remove_wildcard_back(path)

# ============================================================
# 5. Закомментировать admin/statistics.py (строковые CB)
# ============================================================

stats = ROOT / "bot/routers/admin/statistics.py"
if stats.exists():
    text = stats.read_text(encoding="utf-8")
    write(stats, "# TEMP DISABLED\n" + "\n".join("# " + l for l in text.splitlines()))

print("\n✅ AUTO-FIX COMPLETED")
