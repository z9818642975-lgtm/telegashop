# add_file_headers.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent  # клади скрипт в корень проекта


def normalize_path(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def process_file(py_file: Path):
    rel_path = normalize_path(py_file)
    header = f"# {rel_path}\n"

    try:
        content = py_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[SKIP] {rel_path}: {e}")
        return

    lines = content.splitlines(keepends=True)

    if lines and lines[0].startswith("# "):
        if lines[0] != header:
            lines[0] = header
    else:
        lines.insert(0, header)

    py_file.write_text("".join(lines), encoding="utf-8")
    print(f"[OK] {rel_path}")


def main():
    for py_file in PROJECT_ROOT.rglob("*.py"):
        # при необходимости исключай venv / .venv / migrations и т.д.
        if any(part.startswith(".") for part in py_file.parts):
            continue
        process_file(py_file)


if __name__ == "__main__":
    main()
