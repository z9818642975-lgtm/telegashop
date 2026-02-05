import re
from pathlib import Path

ROOT = Path("bot")
STAR_RE = re.compile(r"from bot\.constants\.callbacks_\w+ import \*")

errors = []

for file in ROOT.rglob("*.py"):
    try:
        text = file.read_text(encoding="utf-8")
    except Exception:
        continue

    if STAR_RE.search(text):
        errors.append(file)

if errors:
    print("❌ STAR IMPORTS FOUND:\n")
    for f in errors:
        print(" -", f)
    exit(1)

print("✅ No star imports found")
