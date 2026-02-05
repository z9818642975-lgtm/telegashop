from __future__ import annotations

import ast
from pathlib import Path

BOT = Path(__file__).resolve().parents[2] / "bot"

KEYBOARD_DIR = BOT / "keyboards"
ROUTER_DIR = BOT / "routers"

def scan_callbacks_in_keyboards() -> set[str]:
    found = set()
    for file in KEYBOARD_DIR.rglob("*.py"):
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                found.add(node.func.id)
    return found


def scan_callbacks_in_routers() -> set[str]:
    handled = set()
    for file in ROUTER_DIR.rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr == "filter":
                if isinstance(node.value, ast.Name):
                    handled.add(node.value.id)
    return handled


def main():
    kb = scan_callbacks_in_keyboards()
    rt = scan_callbacks_in_routers()

    missing = sorted(cb for cb in kb if cb.endswith("CB") and cb not in rt)

    out = BOT / "routers/_todo_callbacks.py"
    lines = [
        "from aiogram import Router",
        "from aiogram.types import CallbackQuery",
        "",
        "router = Router(name='todo_callbacks')",
        "",
    ]

    for cb in missing:
        lines += [
            f"@router.callback_query({cb}.filter())",
            f"async def todo_{cb.lower()}(cb: CallbackQuery):",
            f"    # TODO: implement handler for {cb}",
            "    await cb.answer('⏳ В разработке')",
            "",
        ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"📝 GENERATED: {out}")
    print(f"📌 TODO handlers: {len(missing)}")


if __name__ == "__main__":
    main()
