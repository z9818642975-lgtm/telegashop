# scripts/fix_mojibake.py
from pathlib import Path
import re

ROOT = Path(".")
EXTS = {".py", ".yml", ".yaml", ".sql", ".md", ".txt"}

# сигнатуры CP1251->UTF8 mojibake (ASCII-safe)
BAD_RE = re.compile(
    r"(Рџ|Рё|Рё|СЃ|С‚|Р°С|РѕР|РµР|рџ|вњ)"
)

CYRILLIC_RE = re.compile(r"[А-Яа-я]")

def try_fix(line: str) -> str | None:
    """
    UTF-8(with BOM) -> CP1251 -> UTF-8
    """
    try:
        fixed = line.encode("cp1251").decode("utf-8-sig")
    except Exception:
        return None

    # safety checks
    if BAD_RE.search(fixed):
        return None
    if not CYRILLIC_RE.search(fixed):
        return None

    return fixed

def process_file(path: Path):
    changed = False
    lines = path.read_text(
        encoding="utf-8",
        errors="ignore"
    ).splitlines(keepends=True)

    for i, line in enumerate(lines):
        if BAD_RE.search(line):
            fixed = try_fix(line)
            if fixed:
                lines[i] = fixed
                changed = True

    if changed:
        path.write_text("".join(lines), encoding="utf-8")
        print(f"✅ FIXED {path}")

for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix in EXTS:
        process_file(path)

