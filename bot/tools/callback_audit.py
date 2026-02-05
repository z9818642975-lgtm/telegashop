import pathlib
import re
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]

CALLBACK_FILTER = re.compile(r'@router\.callback_query\(([^)]*)\)')
PACK_CALL = re.compile(r'\.pack\(\)')

results = {
    "filters": defaultdict(list),   # CB -> files
    "packs": defaultdict(list),     # CB -> files
    "strings": [],                  # raw callback_data="..."
}


def scan_file(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")

    # 1. callback_query(SomeCB.filter())
    for match in CALLBACK_FILTER.findall(text):
        if ".filter()" in match:
            cb = match.split(".filter()")[0].strip()
            results["filters"][cb].append(path)

    # 2. .pack()
    if ".pack()" in text:
        for line in text.splitlines():
            if ".pack()" in line:
                results["packs"][line.strip()].append(path)

    # 3. callback_data="..."
    if "callback_data=" in text:
        results["strings"].append(path)


for py in ROOT.rglob("*.py"):
    if any(x in py.parts for x in (".venv", "__pycache__")):
        continue
    scan_file(py)


print("\n=== CALLBACK FILTERS (handlers) ===")
for cb, files in results["filters"].items():
    print(f"{cb}")
    for f in files:
        print(f"  - {f}")

print("\n=== PACK() USAGE (buttons) ===")
for line, files in results["packs"].items():
    print(f"{line}")
    for f in files:
        print(f"  - {f}")

print("\n=== RAW callback_data= (❌ forbidden) ===")
for f in results["strings"]:
    print(f"  - {f}")