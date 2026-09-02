#!/usr/bin/env python3
"""Reject ambiguous single-letter aliases for workflow skills."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".dsl"}
EXCLUDED_DIRS = {"__pycache__", ".git", ".structurizr"}

PATTERNS = [
    ("single_letter_skill_name", re.compile(r"(?i)\bskill\s+[abcde](?![-\w])")),
    ("single_letter_invoke", re.compile(r"(?i)\b(?:invoke|run|continue)\s+[abcde](?![-\w])")),
    ("single_letter_handoff", re.compile(r"(?i)\b(?:handoff|hand-off)\s+(?:to\s+)?[abcde](?![-\w])")),
    ("single_letter_next_action", re.compile(r"(?i)\bnext\s+action\s*[:=-]?\s*(?:run\s+)?[abcde](?![-\w])")),
    ("single_letter_workflow_label", re.compile(r"(?i)\b(?:set\s+handoff\s+to|do\s+not\s+invoke)\s+[abcde](?![-\w])")),
]


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_root", type=Path)
    args = parser.parse_args()
    root = args.skill_root.resolve()
    errors = []
    for path in iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for code, pattern in PATTERNS:
                match = pattern.search(line)
                if match:
                    errors.append({
                        "code": code,
                        "file": str(path.relative_to(root)),
                        "line": line_no,
                        "text": line.strip(),
                        "match": match.group(0),
                    })
    result = {"passed": not errors, "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
