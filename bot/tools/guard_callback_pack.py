# bot/tools/guard_callback_pack.py
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2] / "bot"
ERRORS = []

def check_file(path: Path):
    text = path.read_text(encoding="utf-8")

    if "callback_data=" in text:
        for line_no, line in enumerate(text.splitlines(), 1):
            if "callback_data=" in line and ".pack()" not in line:
                ERRORS.append((path, line_no, "callback_data без .pack()"))

    if "F.data ==" in text:
        ERRORS.append((path, "?", "F.data == запрещён"))

def main():
    for file in BASE.rglob("admin/**/*.py"):
        check_file(file)

    if ERRORS:
        print("❌ CALLBACK PACK GUARD FAILED")
        for f, l, m in ERRORS:
            print(f"{f}:{l} → {m}")
        sys.exit(1)

    print("✅ CALLBACK PACK GUARD PASSED")

if __name__ == "__main__":
    main()

# noqa: F401,F403,E402,E741
