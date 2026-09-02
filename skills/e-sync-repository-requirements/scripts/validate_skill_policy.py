#!/usr/bin/env python3
"""Validate the core safety policy of e-sync-repository-requirements."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_PHRASES = {
    "full_identifier": "Never use single-letter skill aliases.",
    "approval": "Require explicit human approval before every remote write",
    "no_delete": "Never delete an issue",
    "no_close": "Never close or reopen an issue",
    "no_labels": "Do not manage labels.",
    "no_subissue_write": "Do not create or modify subissue relationships.",
    "no_persistent_sync": "Do not create persistent synchronization documents or statistics.",
    "no_context_no_create": "Do not create an issue without sufficient remote context.",
    "minimal_creation": "Reuse work before creating work",
}

def read_text_files(root: Path) -> str:
    parts: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml", ".py"}:
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


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

    skill = skill_path.read_text(encoding="utf-8")
    all_text = read_text_files(root)
    lower = all_text.casefold()

    if not re.search(r"^name:\s*e-sync-repository-requirements\s*$", skill, flags=re.MULTILINE):
        errors.append({"code": "wrong_name", "detail": "Expected exact lowercase skill name"})

    for code, phrase in REQUIRED_PHRASES.items():
        if phrase not in skill:
            errors.append({"code": f"missing_{code}", "detail": phrase})

    forbidden_files = {"repository_sync_plan.md", "issue_registry.md", "sync_history.md"}
    for path in root.rglob("*"):
        if path.is_file() and path.name.casefold() in forbidden_files:
            errors.append({"code": "forbidden_artifact_file", "detail": str(path)})

    policy_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [skill_path, *sorted((root / "references").glob("*.md"))]
        if path.exists()
    )
    for pattern, label in [(r"\bSYNC-\d{3,}\b", "visible synchronization identifier"), (r"\bOP-\d{3,}\b", "visible operation identifier")]:
        match = re.search(pattern, policy_text, flags=re.IGNORECASE)
        if match:
            errors.append({"code": "forbidden_visible_identifier", "detail": label, "value": match.group(0)})

    alias_patterns = [
        r"\bRun\s+[ABCDE]\b",
        r"\bContinue\s+[ABCDE]\b",
        r"`[ABCDE]`\s+(?:skill|workflow)",
    ]
    for pattern in alias_patterns:
        match = re.search(pattern, all_text)
        if match:
            errors.append({"code": "single_letter_alias", "detail": match.group(0)})

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
