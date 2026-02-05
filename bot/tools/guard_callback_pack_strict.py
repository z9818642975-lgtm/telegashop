from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PROJECT_ROOT = ROOT / "bot"
IGNORED_PARTS = {"__pycache__", ".bak", ".disabled"}

ERRORS: List[str] = []


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def check_file(path: Path) -> None:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        # something.pack()
        if not isinstance(node.func, ast.Attribute):
            continue

        if node.func.attr != "pack":
            continue

        value = node.func.value

        # ❌ callback_data=().pack()
        if isinstance(value, ast.Tuple):
            ERRORS.append(f"{path}: callback_data=().pack() — ЗАПРЕЩЕНО")
            continue

        # ❌ "text".pack() / var.pack()
        if not isinstance(value, ast.Call):
            ERRORS.append(
                f"{path}: .pack() вызван не на CallbackData (node={ast.dump(value)})"
            )


def main() -> None:
    for py in PROJECT_ROOT.rglob("*.py"):
        if is_ignored(py):
            continue
        check_file(py)

    if ERRORS:
        print("\n❌ CALLBACK PACK STRICT GUARD FAILED\n")
        for e in ERRORS:
            print(" -", e)
        sys.exit(1)

    print("✅ CALLBACK PACK STRICT GUARD PASSED")


if __name__ == "__main__":
    main()
