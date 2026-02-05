from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2] / "bot"

CALLBACK_MODULES = {
    "Admin": "bot.constants.callbacks_admin",
    "Operator": "bot.constants.callbacks_operator",
    "Client": "bot.constants.callbacks_client",
    "Back": "bot.constants.callbacks_common",
}

def collect_used_callbacks(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    used = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id.endswith("CB") or node.func.id.startswith(
                ("Admin", "Client", "Operator")
            ):
                used.add(node.func.id)
    return used


def main():
    files = list(PROJECT_ROOT.rglob("*.py"))
    for file in files:
        text = file.read_text(encoding="utf-8")
        if "import *" not in text:
            continue

        used = collect_used_callbacks(file)
        if not used:
            continue

        imports = defaultdict(set)
        for cb in used:
            for prefix, module in CALLBACK_MODULES.items():
                if cb.startswith(prefix):
                    imports[module].add(cb)

        import_lines = []
        for module, names in imports.items():
            import_lines.append(
                f"from {module} import {', '.join(sorted(names))}"
            )

        cleaned = []
        for line in text.splitlines():
            if "import *" not in line:
                cleaned.append(line)

        new_text = "\n".join(import_lines) + "\n\n" + "\n".join(cleaned)
        file.write_text(new_text, encoding="utf-8")
        print(f"[FIX EXPLICIT IMPORT] {file}")


if __name__ == "__main__":
    main()
