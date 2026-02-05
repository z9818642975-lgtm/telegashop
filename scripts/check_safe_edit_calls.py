# scripts/check_safe_edit_calls.py
import ast
import pathlib

ROOT = pathlib.Path("bot")


class SafeEditVisitor(ast.NodeVisitor):
    def __init__(self, file: pathlib.Path):
        self.file = file

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "safe_edit_text":
            if len(node.args) > 1:
                print(
                    f"❌ {self.file}:{node.lineno}:{node.col_offset} "
                    f"safe_edit_text called with {len(node.args)} positional args"
                )
        self.generic_visit(node)


def main():
    errors = 0
    for file in ROOT.rglob("*.py"):
        try:
            tree = ast.parse(file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        visitor = SafeEditVisitor(file)
        visitor.visit(tree)

    print("\nAST scan completed.")


if __name__ == "__main__":
    main()

