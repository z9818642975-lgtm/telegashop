# bot/tools/guard_imports.py
import ast
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2] / "bot"
ERRORS = []

FORBIDDEN = {
    "client": ["admin", "operator"],
    "operator": ["admin", "client"],
    "admin": ["client", "operator"],
}

def check_file(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.names[0].name == "*":
                ERRORS.append((path, node.lineno, "wildcard import запрещён"))

            module = node.module or ""
            for side, banned in FORBIDDEN.items():
                if f".{side}." in str(path):
                    for b in banned:
                        if module.startswith(f"bot.{b}"):
                            ERRORS.append((path, node.lineno, f"{side} импортирует {b}"))

def main():
    for file in BASE.rglob("admin/**/*.py"):
        check_file(file)

    if ERRORS:
        print("❌ IMPORT GUARD FAILED")
        for f, l, m in ERRORS:
            print(f"{f}:{l} → {m}")
        sys.exit(1)

    print("✅ IMPORT GUARD PASSED")

if __name__ == "__main__":
    main()

# noqa: F401,F403,E402,E741
