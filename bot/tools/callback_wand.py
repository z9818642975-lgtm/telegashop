# bot/tools/callback_wand.py
import ast
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

ROOT = Path("bot")
CALLBACKS = ROOT / "constants" / "callbacks.py"
REPORT = Path("callback_wand_report.md")


# =========================
# Schema
# =========================

class CB:
    def __init__(self, name: str, fields: list[str]):
        self.name = name
        self.fields = fields


def load_schema() -> Dict[str, CB]:
    tree = ast.parse(CALLBACKS.read_text(encoding="utf-8"))
    schema = {}

    for n in tree.body:
        if not isinstance(n, ast.ClassDef):
            continue

        if not any(
            isinstance(b, ast.Name) and b.id == "CallbackData"
            for b in n.bases
        ):
            continue

        fields = [
            x.target.id
            for x in n.body
            if isinstance(x, ast.AnnAssign)
        ]

        schema[n.name] = CB(n.name, fields)

    return schema


# =========================
# Fixer
# =========================

class Fixer(ast.NodeTransformer):
    def __init__(self, schema, file, mode, report):
        self.schema = schema
        self.file = file
        self.mode = mode
        self.report = report
        self.changed = False

    def visit_Call(self, node):
        self.generic_visit(node)

        if not isinstance(node.func, ast.Name):
            return node

        if node.func.id != "InlineKeyboardButton":
            return node

        for kw in node.keywords:
            if kw.arg != "callback_data":
                continue

            if isinstance(kw.value, ast.Name):
                name = kw.value.id

                if name not in self.schema:
                    self.report.append(
                        f"- {self.file}: unknown callback `{name}`"
                    )
                    continue

                cb = self.schema[name]

                if cb.fields:
                    self.report.append(
                        f"- {self.file}: `{name}` требует {cb.fields}"
                    )
                    continue

                if self.mode == "fix":
                    kw.value = ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Name(name, ast.Load()),
                                args=[],
                                keywords=[],
                            ),
                            attr="pack",
                            ctx=ast.Load(),
                        ),
                        args=[],
                        keywords=[],
                    )
                    self.changed = True

        return node


# =========================
# Backup
# =========================

def backup():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = ROOT / ".callback_backup" / ts
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".callback_backup"))
    print(f"🧷 backup → {dst}")


# =========================
# Main
# =========================

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    if mode not in {"check", "fix", "report"}:
        print("usage: callback_wand.py [check|fix|report]")
        sys.exit(1)

    schema = load_schema()
    report: List[str] = []

    if mode == "fix":
        backup()

    for py in ROOT.rglob("*.py"):
        if py == CALLBACKS:
            continue

        tree = ast.parse(py.read_text(encoding="utf-8"))
        fixer = Fixer(schema, py, mode, report)
        new = fixer.visit(tree)

        if fixer.changed:
            py.write_text(ast.unparse(new), encoding="utf-8")
            print("✔ fixed", py)

    if report:
        REPORT.write_text(
            "# CALLBACK WAND REPORT\n\n"
            "## ❌ Требуется ручная правка\n\n"
            + "\n".join(report),
            encoding="utf-8",
        )
        print("📄 report →", REPORT)

    if mode == "check" and report:
        print("⛔ callback contract broken")
        sys.exit(1)

    print("✅ callback wand done")


if __name__ == "__main__":
    main()