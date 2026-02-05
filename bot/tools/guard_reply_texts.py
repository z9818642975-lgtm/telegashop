# bot/tools/guard_reply_texts.py
# python bot/tools/guard_reply_texts.py

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # bot/
TARGET_DIRS = [
    ROOT / "keyboards",
    ROOT / "routers",
]

# =========================
# НАСТРОЙКА ПРАВИЛ
# =========================

ROLE_PREFIX = {
    "admin": "А ",
    "operator": "О ",
}

ROLE_HINTS = {
    "admin": ["RoleFilter(\"admin\")", "RoleFilter('admin')"],
    "operator": ["RoleFilter(\"operator\")", "RoleFilter('operator')"],
}

TEXT_RE = re.compile(r'F\.text\s*==\s*"([^"]+)"')
IN_LIST_RE = re.compile(r'F\.text\.in_\(\[([^\]]+)\]\)')
REPLY_BTN_RE = re.compile(r'text\s*=\s*"([^"]+)"')

# =========================
# УТИЛИТЫ
# =========================

def detect_role(text: str) -> str | None:
    for role, prefix in ROLE_PREFIX.items():
        if text.startswith(prefix):
            return role
    return None


def add_prefix(role: str, text: str) -> str:
    prefix = ROLE_PREFIX[role]
    if text.startswith(prefix):
        return text
    return prefix + text


def file_contains_role_hint(content: str, role: str) -> bool:
    return any(hint in content for hint in ROLE_HINTS[role])


# =========================
# ОСНОВНАЯ ЛОГИКА
# =========================

errors: list[str] = []
changed_files = 0

for base in TARGET_DIRS:
    for path in base.rglob("*.py"):
        content = path.read_text(encoding="utf-8")
        original = content

        for role in ("admin", "operator"):
            if not file_contains_role_hint(content, role):
                continue

            # --- F.text == "..."
            def repl_text(m):
                old = m.group(1)
                new = add_prefix(role, old)
                return f'F.text == "{new}"'

            content = TEXT_RE.sub(repl_text, content)

            # --- F.text.in_(["...", "..."])
            def repl_list(m):
                items = m.group(1)
                new_items = []
                for part in items.split(","):
                    part = part.strip()
                    if part.startswith('"') and part.endswith('"'):
                        txt = part[1:-1]
                        txt = add_prefix(role, txt)
                        new_items.append(f'"{txt}"')
                    else:
                        new_items.append(part)
                return f'F.text.in_([{", ".join(new_items)}])'

            content = IN_LIST_RE.sub(repl_list, content)

            # --- reply keyboard buttons
            def repl_reply(m):
                old = m.group(1)
                new = add_prefix(role, old)
                return f'text="{new}"'

            content = REPLY_BTN_RE.sub(repl_reply, content)

        if content != original:
            path.write_text(content, encoding="utf-8")
            changed_files += 1

# =========================
# GUARD: одинаковые тексты
# =========================

texts_by_role: dict[str, set[str]] = {"admin": set(), "operator": set()}

for base in TARGET_DIRS:
    for path in base.rglob("*.py"):
        content = path.read_text(encoding="utf-8")

        for role, prefix in ROLE_PREFIX.items():
            for m in REPLY_BTN_RE.finditer(content):
                txt = m.group(1)
                if txt.startswith(prefix):
                    texts_by_role[role].add(txt[len(prefix):])

intersection = texts_by_role["admin"] & texts_by_role["operator"]

if intersection:
    print("❌ GUARD FAILED: одинаковые кнопки у ADMIN и OPERATOR:")
    for t in sorted(intersection):
        print("   ", t)
    sys.exit(1)

print(f"✅ OK. Изменено файлов: {changed_files}")
print("🛡 Повторов между ролями нет.")
# noqa: F401,F403,E402,E741
