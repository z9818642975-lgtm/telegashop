import os
import re

KEYBOARD_DIRS = [
    "bot/keyboards/client",
    "bot/keyboards/operator",
    "bot/keyboards/admin",
]

ROUTER_DIR = "bot/routers"

texts = set()
handlers = set()

# Тексты кнопок (reply + inline)
TEXT_RE = re.compile(r'text\s*=\s*"([^"]+)"')
HANDLER_RE = re.compile(r'F\.text\s*==\s*"([^"]+)"')

for base in KEYBOARD_DIRS:
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith(".py"):
                code = open(os.path.join(root, f), encoding="utf-8").read()
                texts.update(TEXT_RE.findall(code))

for root, _, files in os.walk(ROUTER_DIR):
    for f in files:
        if f.endswith(".py"):
            code = open(os.path.join(root, f), encoding="utf-8").read()
            handlers.update(HANDLER_RE.findall(code))

missing = texts - handlers

if missing:
    print("🧩 Кнопки без handler’ов:")
    for t in sorted(missing):
        print(" •", t)
    exit(1)

print("✅ Все кнопки имеют handler’ы")
