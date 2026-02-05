import re
from pathlib import Path

ADMIN_DIR = Path("bot/keyboards/admin")

BAD_IMPORT_RE = re.compile(
    r"from bot\.constants\.callbacks_(common|client|operator) import .*"
)

for file in ADMIN_DIR.rglob("*.py"):
    text = file.read_text(encoding="utf-8")
    original = text

    lines = []
    for line in text.splitlines():
        if BAD_IMPORT_RE.match(line):
            continue
        lines.append(line)

    text = "\n".join(lines)

    if text != original:
        file.write_text(text, encoding="utf-8")
        print(f"[FIXED] {file}")

print("✅ Admin keyboards imports cleaned")
