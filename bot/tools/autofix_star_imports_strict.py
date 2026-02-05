from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Set

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BOT = ROOT / "bot"
CALLBACK_MODULES = {
    "admin": "bot.constants.callbacks_admin",
    "client": "bot.constants.callbacks_client",
    "operator": "bot.constants.callbacks_operator",
    "common": "bot.constants.callbacks_common",
}


def extract_used_callbacks(tree: ast.AST) -> Set[str]:
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id.endswith("CB") or node.id.startswith(("Admin", "Client", "Operator")):
                used.add(node.id)
    return used


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "import *" not in text:
        return

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return

    used = extract_used_callbacks(tree)
    if not used:
        return

    module = None
    if "/admin/" in str(path):
        module = CALLBACK_MODULES["admin"]
    elif "/client/" in str(path):
        module = CALLBACK_MODULES["client"]
    elif "/operator/" in str(path):
        module = CALLBACK_MODULES["operator"]
    else:
        module = CALLBACK_MODULES["common"]

    import_line = f"from {module} import {', '.join(sorted(used))}\n"

    lines = []
    for line in text.splitlines():
        if "callbacks_" in line and "import *" in line:
            continue
        lines.append(line)

    new_text = import_line + "\n".join(lines)
    path.write_text(new_text, encoding="utf-8")
    print(f"[FIX STAR] {path}")


def main():
    for py in BOT.rglob("*.py"):
        process_file(py)


if __name__ == "__main__":
    main()
