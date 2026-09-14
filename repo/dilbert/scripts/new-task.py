#!/usr/bin/env python3
"""Create a local note without overwriting; invokes neither models nor Git."""
import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id", help="Letters, numbers, hyphens, underscores; maximum 80 characters")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", args.id):
        parser.error("Invalid ID; example: OPS-123")
    local = Path(__file__).resolve().parents[1]
    root = local.parent
    text = (local / "templates/task.md").read_text(encoding="utf-8")
    notes = root / "thoughts"
    if notes.is_symlink():
        parser.error("thoughts is a symlink; use a repository-local directory")
    dest = notes / args.id
    if dest.is_symlink():
        parser.error("The task directory cannot be a symlink")
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "task.md"
    try:
        with path.open("x", encoding="utf-8") as out:
            out.write(text.replace("__ID__", args.id))
    except FileExistsError:
        parser.exit(1, f"Not overwritten: {path}\n")
    print(f"Created: {path}")
    print("Next: describe the request and confirm the oracle with Dilbert.")


if __name__ == "__main__":
    main()
