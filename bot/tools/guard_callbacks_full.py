from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Dict, Set

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PROJECT_ROOT = ROOT / "bot"

CALLBACK_CLASSES: Dict[str, str] = {}
HANDLED_IN_ROUTERS: Set[str] = set()
USED_IN_KEYBOARDS: Set[str] = set()
BROKEN_FILES: Set[Path] = set()


# =========================================================
# SCAN CALLBACK DEFINITIONS
# =========================================================

def scan_callbacks() -> None:
    for file in (PROJECT_ROOT / "constants").rglob("callbacks_*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except SyntaxError:
            BROKEN_FILES.add(file)
            continue

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "CallbackData":
                        CALLBACK_CLASSES[node.name] = file.name


# =========================================================
# SCAN ROUTERS
# =========================================================

def scan_routers() -> Set[str]:
    handled = set()

    for file in (PROJECT_ROOT / "routers").rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except SyntaxError:
            BROKEN_FILES.add(file)
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == "filter":
                        if isinstance(node.func.value, ast.Name):
                            handled.add(node.func.value.id)

    return handled


# =========================================================
# SCAN KEYBOARDS
# =========================================================

def scan_keyboards() -> Set[str]:
    used = set()

    for file in (PROJECT_ROOT / "keyboards").rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except SyntaxError:
            BROKEN_FILES.add(file)
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr == "pack":
                    if isinstance(node.func.value, ast.Call):
                        if isinstance(node.func.value.func, ast.Name):
                            used.add(node.func.value.func.id)

    return used


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    scan_callbacks()
    global HANDLED_IN_ROUTERS, USED_IN_KEYBOARDS

    HANDLED_IN_ROUTERS = scan_routers()
    USED_IN_KEYBOARDS = scan_keyboards()

    missing_handlers = USED_IN_KEYBOARDS - HANDLED_IN_ROUTERS
    unused_callbacks = set(CALLBACK_CLASSES) - USED_IN_KEYBOARDS

    if BROKEN_FILES:
        print("\n⚠️ ПРОПУЩЕНЫ ФАЙЛЫ С SYNTAX ERROR:")
        for f in sorted(BROKEN_FILES):
            print(" -", f)

    if missing_handlers:
        print("\n❌ CALLBACK БЕЗ HANDLER’ОВ:")
        for cb in sorted(missing_handlers):
            print(" -", cb)
        print("\n👉 Нужно добавить router.callback_query(...)\n")
        sys.exit(1)

    if unused_callbacks:
        print("\n⚠️ CALLBACK НЕ ИСПОЛЬЗУЕТСЯ:")
        for cb in sorted(unused_callbacks):
            print(" -", cb)

    print("\n✅ CALLBACK CONTRACT OK")


if __name__ == "__main__":
    main()
