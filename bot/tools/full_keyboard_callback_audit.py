#!/usr/bin/env python3
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # bot/tools/ -> project root
BOT_ROOT = PROJECT_ROOT / "bot"

TEXT_BUTTON_RE = re.compile(r'KeyboardButton\s*\(\s*text\s*=\s*[\'"](.+?)[\'"]')
F_TEXT_RE = re.compile(r'F\.text\s*==\s*[\'"](.+?)[\'"]')
F_TEXT_IN_RE = re.compile(r'F\.text\.in_\(\s*\[(.*?)\]\s*\)', re.S)

CALLBACK_PACK_RE = re.compile(r'\.pack\(\)')
CALLBACK_CLASS_RE = re.compile(r'callback_data\s*=\s*([A-Za-z0-9_]+)\(')
CALLBACK_HANDLER_RE = re.compile(r'@router\.callback_query\(\s*([A-Za-z0-9_]+)')

def read_file_utf8_fix(path: Path):
    try:
        return path.read_text(encoding="utf-8"), "utf-8"
    except UnicodeDecodeError:
        raw = path.read_bytes()
        try:
            text = raw.decode("cp1251")
            backup = path.with_suffix(path.suffix + ".bak")
            if not backup.exists():
                backup.write_bytes(raw)
            path.write_text(text, encoding="utf-8")
            return text, "converted"
        except Exception:
            return None, "broken"

def scan_files():
    reply_buttons = set()
    f_texts = set()
    callbacks_buttons = set()
    callbacks_handlers = set()
    encoding_issues = []

    for path in BOT_ROOT.rglob("*.py"):
        text, status = read_file_utf8_fix(path)
        if status != "utf-8":
            encoding_issues.append({"file": str(path), "status": status})
        if not text:
            continue

        # ReplyKeyboard
        for m in TEXT_BUTTON_RE.findall(text):
            reply_buttons.add(m.strip())

        for m in F_TEXT_RE.findall(text):
            f_texts.add(m.strip())

        for block in F_TEXT_IN_RE.findall(text):
            for val in re.findall(r'[\'"](.+?)[\'"]', block):
                f_texts.add(val.strip())

        # Inline callbacks
        for m in CALLBACK_CLASS_RE.findall(text):
            callbacks_buttons.add(m)

        for m in CALLBACK_HANDLER_RE.findall(text):
            callbacks_handlers.add(m)

    return {
        "reply_buttons": sorted(reply_buttons),
        "f_texts": sorted(f_texts),
        "callbacks_buttons": sorted(callbacks_buttons),
        "callbacks_handlers": sorted(callbacks_handlers),
        "encoding": encoding_issues,
    }

def main():
    data = scan_files()

    reply_without_handlers = set(data["reply_buttons"]) - set(data["f_texts"])
    handlers_without_buttons = set(data["f_texts"]) - set(data["reply_buttons"])

    callbacks_without_handlers = set(data["callbacks_buttons"]) - set(data["callbacks_handlers"])
    handlers_without_callbacks = set(data["callbacks_handlers"]) - set(data["callbacks_buttons"])

    report = {
        "reply": {
            "buttons_without_handlers": sorted(reply_without_handlers),
            "handlers_without_buttons": sorted(handlers_without_buttons),
        },
        "callbacks": {
            "callbacks_without_handlers": sorted(callbacks_without_handlers),
            "handlers_without_callbacks": sorted(handlers_without_callbacks),
        },
        "encoding_issues": data["encoding"],
    }

    print("\n=== REPLY KEYBOARD AUDIT ===")
    print("❌ Buttons without F.text:")
    for x in report["reply"]["buttons_without_handlers"]:
        print("  -", x)

    print("\n❌ F.text without buttons:")
    for x in report["reply"]["handlers_without_buttons"]:
        print("  -", x)

    print("\n=== CALLBACK AUDIT ===")
    print("❌ Callbacks without handlers:")
    for x in report["callbacks"]["callbacks_without_handlers"]:
        print("  -", x)

    print("\n❌ Handlers without callbacks:")
    for x in report["callbacks"]["handlers_without_callbacks"]:
        print("  -", x)

    if report["encoding_issues"]:
        print("\n=== ENCODING FIXES ===")
        for x in report["encoding_issues"]:
            print(f"⚠ {x['file']} → {x['status']}")

    out = PROJECT_ROOT / "audit_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📄 JSON report: {out}")

if __name__ == "__main__":
    main()