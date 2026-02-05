from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Dict, Set

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BOT = ROOT / "bot"
OUT = BOT / "routers" / "_todo_callbacks.py"

CALLBACKS: Dict[str, str] = {}
HANDLED: Set[str] = set()


def scan_callbacks():
    for f in (BOT / "constants").rglob("callbacks_*.py"):
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                CALLBACKS[node.name] = f.name


def scan_routers():
    for f in (BOT / "routers").rglob("*.py"):
        if f.name.startswith("_todo"):
            continue
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr == "filter":
                if isinstance(node.value, ast.Name):
                    HANDLED.add(node.value.id)


def main():
    scan_callbacks()
    scan_routers()

    missing = sorted(set(CALLBACKS) - HANDLED)
    if not missing:
        print("✅ NO MISSING CALLBACK HANDLERS")
        return

    lines = [
        "from aiogram import Router",
        "from aiogram.types import CallbackQuery",
        "from sqlalchemy.ext.asyncio import AsyncSession",
        "",
        "# AUTO-GENERATED TODO HANDLERS",
        "router = Router(name='todo_callbacks')",
        "",
    ]

    for cb in missing:
        lines.extend(
            [
                f"@router.callback_query({cb}.filter())",
                f"async def todo_{cb.lower()}(",
                "    cb: CallbackQuery,",
                f"    callback_data: {cb},",
                "    session: AsyncSession,",
                "):",
                f"    # TODO: implement handler for {cb}",
                "    await cb.answer('⏳ В разработке')",
                "",
            ]
        )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"📝 GENERATED: {OUT}")
    print(f"📌 TODO handlers: {len(missing)}")


if __name__ == "__main__":
    main()
