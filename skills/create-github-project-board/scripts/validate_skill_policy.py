#!/usr/bin/env python3
"""Validate safety policy for create-github-project-board."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_PHRASES = {
    "name": "name: create-github-project-board",
    "approval": "Require explicit human approval before every remote mutation",
    "recreate": "Do not use `gh project copy`",
    "no_product_issues": "Never create product issues",
    "no_delete": "Never close or delete a Project.",
    "triage": "New Issues -> Triage -> Icebox -> Product Backlog",
    "sync_handoff": "route back to `e-sync-repository-requirements`",
}


def read_policy_files(root: Path) -> str:
    paths = [root / "SKILL.md"]
    references = root / "references"
    if references.exists():
        paths.extend(sorted(references.glob("*.md")))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", nargs="?", default=".", type=Path)
    args = parser.parse_args()

    root = args.skill_dir.resolve()
    skill_path = root / "SKILL.md"
    errors: list[dict[str, str]] = []

    if not skill_path.exists():
        errors.append({"code": "missing_skill", "detail": str(skill_path)})
        print(json.dumps({"passed": False, "errors": errors}, indent=2))
        return 1

    policy = read_policy_files(root)

    for code, phrase in REQUIRED_PHRASES.items():
        if phrase not in policy:
            errors.append({"code": f"missing_{code}", "detail": phrase})

    forbidden = [
        (r"(?<!not use `)\bgh\s+project\s+copy\b", "project copy command must not be instructed"),
        (r"\bgh\s+project\s+field-delete\b", "field deletion command must not be instructed"),
        (r"\bgh\s+project\s+(?:close|delete)\b", "project close/delete command must not be instructed"),
    ]
    for pattern, detail in forbidden:
        match = re.search(pattern, policy, flags=re.IGNORECASE)
        if match:
            errors.append({"code": "forbidden_policy", "detail": detail, "value": match.group(0)})

    result = {
        "passed": not errors,
        "skill_dir": str(root),
        "checked_required_phrases": sorted(REQUIRED_PHRASES),
        "errors": errors,
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
