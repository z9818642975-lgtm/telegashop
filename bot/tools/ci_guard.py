import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

EXCLUDE_FILES = {
    "ci_guard.py",
    "guard_callbacks.py",
}

FAIL = False


def error(msg):
    global FAIL
    FAIL = True
    print(f"[CI-GUARD] ❌ {msg}")


for p in ROOT.rglob("*.py"):
    if p.name in EXCLUDE_FILES:
        continue

    text = p.read_text(encoding="utf-8", errors="ignore")

    # Запрещён wildcard callback_query
    if "callback_query(True)" in text:
        error(f"callback_query(True) in {p}")

    # Запрещён raw callback_data
    if "callback_data=" in text and ".pack()" not in text:
        error(f"raw callback_data in {p}")


if FAIL:
    sys.exit(1)

print("[CI-GUARD] ✅ OK")