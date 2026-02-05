import os
import re

PROJECT_ROOT = os.path.abspath(".")
TARGET_EXTENSIONS = (".py",)

REPLACEMENTS = [
    # imports
    (
        r"from\s+bot\.keyboards\.reply\.client_menu\s+import\s+client_main_menu_kb",
        "from bot.keyboards.client.main import client_main_menu_kb",
    ),
    (
        r"from\s+bot\.keyboards\.admin\.panel\s+import\s+admin_panel_kb",
        "from bot.keyboards.admin.main import admin_main_menu_kb",
    ),

    # remove dead callback imports
    (
        r"from\s+bot\.constants\.callbacks_client\s+import\s+ClientBackMenu\s*\n?",
        "",
    ),
    (
        r"from\s+bot\.constants\.callbacks_client\s+import\s+ClientBackCatalog\s*\n?",
        "",
    ),

    # function rename
    (
        r"\bclient_main_menu\(\)",
        "client_main_menu_kb()",
    ),

    # operator texts (optional but safe)
    (
        r"Выйти на смену",
        "🟢 Начать смену",
    ),
    (
        r"Закрыть смену",
        "🔴 Завершить смену",
    ),
]


def process_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    modified = original
    for pattern, replacement in REPLACEMENTS:
        modified = re.sub(pattern, replacement, modified)

    if modified != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(modified)
        return True

    return False


def main():
    changed_files = []

    for root, _, files in os.walk(PROJECT_ROOT):
        for name in files:
            if name.endswith(TARGET_EXTENSIONS):
                path = os.path.join(root, name)
                if process_file(path):
                    changed_files.append(path)

    print("✅ Автозамена завершена")
    print(f"Изменено файлов: {len(changed_files)}")
    for f in changed_files:
        print(" •", f)


if __name__ == "__main__":
    main()