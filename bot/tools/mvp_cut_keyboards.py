from pathlib import Path

# Кнопки, которые в MVP не поддерживаются
UNSUPPORTED_CB_NAMES = [
    "ClientDeliveryPrice",
    "ClientPickupConfirm",
    "ClientPickupSelect",
    "OperatorHeartbeatCB",
]

KEYBOARD_DIRS = [
    Path("bot/keyboards/client"),
    Path("bot/keyboards/operator"),
    Path("bot/keyboards/admin"),
]

for d in KEYBOARD_DIRS:
    for file in d.glob("*.py"):
        text = file.read_text(encoding="utf-8")
        original = text

        for name in UNSUPPORTED_CB_NAMES:
            if name in text:
                lines = [
                    line for line in text.splitlines()
                    if name not in line
                ]
                text = "\n".join(lines)

        if text != original:
            file.write_text(text, encoding="utf-8")
            print(f"[MVP CUT] {file}")

print("✅ MVP cut complete")
