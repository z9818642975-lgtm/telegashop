# scripts/check_render_calls.py
import ast
import pathlib

ROOT = pathlib.Path("bot")


class RenderCallVisitor(ast.NodeVisitor):
    def __init__(self, filename: pathlib.Path):
        self.filename = filename

    def visit_Call(self, node: ast.Call):
        # render_*
        if isinstance(node.func, ast.Name) and node.func.id.startswith("render_"):
            if not node.args:
                return

            first_arg = node.args[0]

            # ❌ render_xxx(cb, ...)
            if isinstance(first_arg, ast.Name):
                if first_arg.id in {"cb", "callback", "event"}:
                    print(
                        f"❌ {self.filename}:{node.lineno}:{node.col_offset} "
                        f"{node.func.id} called with `{first_arg.id}` (expected Message)"
                    )

        self.generic_visit(node)


def main():
    errors = []

    for path in ROOT.rglob("*.py"):
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as e:
            errors.append(f"⚠ SYNTAX ERROR in {path}:{e.lineno} → {e.msg}")
            continue
        except IndentationError as e:
            errors.append(f"⚠ INDENT ERROR in {path}:{e.lineno} → {e.msg}")
            continue

        RenderCallVisitor(path).visit(tree)

    print("\nAST scan completed.")

    if errors:
        print("\n⚠ Files with syntax errors (must be fixed separately):")
        for e in errors:
            print(e)


if __name__ == "__main__":
    main()
