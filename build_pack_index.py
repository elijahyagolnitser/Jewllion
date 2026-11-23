"""Build the public pack catalog without copying question or answer banks."""

import argparse
import json
from pathlib import Path
import re


def build_index(pack_dir):
    entries = []
    paths = sorted(
        pack_dir.glob("*.json"),
        key=lambda p: [(1, int(s)) if s.isdigit() else (0, s.lower())
                       for s in re.split(r"(\d+)", p.name)],
        reverse=True,
    )
    for path in paths:
        if path.name == "index.json":
            continue
        if any(c in path.name for c in "\\?#"):
            raise ValueError(f"{path.name}: filenames cannot contain backslash, ? or #")
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        pack = data.get("pack", data) if isinstance(data, dict) else None
        if not isinstance(pack, dict):
            raise ValueError(f"{path.name}: expected a pack object")
        title, description = pack.get("title"), pack.get("description", "")
        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 80:
            raise ValueError(f"{path.name}: title must contain 1-80 characters")
        if not isinstance(description, str) or len(description.strip()) > 300:
            raise ValueError(f"{path.name}: description must contain at most 300 characters")
        questions = pack.get("questions")
        if not isinstance(questions, list) or not 1 <= len(questions) <= 200:
            raise ValueError(f"{path.name}: expected 1-200 questions")
        entries.append({
            "file": path.name, "title": title.strip(), "description": description.strip(),
            "questions": len(questions),
        })
    return {"version": 1, "packs": entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packs", type=Path, default=Path(__file__).parent / "packs")
    args = parser.parse_args()
    if not args.packs.is_dir():
        parser.error(f"Pack directory does not exist: {args.packs}")
    # Validate every entry before replacing the catalog.
    contents = json.dumps(build_index(args.packs), ensure_ascii=False, indent=2) + "\n"
    (args.packs / "index.json").write_text(contents, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
