# bot/tools/guard_fstrings.py
import ast
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] / "bot"
ERRORS = []

class FStringVisitor(ast.NodeVisitor):
    def visit_JoinedStr(self, node):
        has_formatted = any(isinstance(v, ast.FormattedValue) for v in node.values)
        if not has_formatted:
            ERRORS.append((node.lineno, "f-string without variables"))
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "format":
                ERRORS.append((node.lineno, "string.format() запрещён, используй f-string"))
        self.generic_visit(node)

def check_file(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        FStringVisitor().visit(tree)
    except SyntaxError as e:
        ERRORS.append((e.lineno, f"SyntaxError: {e.msg}"))

def main():
    for file in BASE_DIR.rglob("admin/*.py"):
        check_file(file)

    if ERRORS:
        print("❌ F-STRING GUARD FAILED")
        for line, msg in ERRORS:
            print(f"  line {line}: {msg}")
        sys.exit(1)

    print("✅ F-STRING GUARD PASSED")

if __name__ == "__main__":
    main()
# noqa: F401,F403,E402,E741
