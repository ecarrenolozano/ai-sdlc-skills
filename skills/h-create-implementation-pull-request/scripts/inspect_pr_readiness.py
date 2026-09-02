#!/usr/bin/env python3
"""Inspect local readiness for an implementation pull request."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ISSUE_RE = re.compile(r"(?:#|US-)(\d{1,6})")
TRACKING_DOCS = (
    "sdlc_docs/trace_workflow.md",
    "sdlc_docs/03_implementation/backlog_priority.md",
)


def run_git(root: Path, args: list[str]) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError) as error:
        return 1, "", str(error)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def git_lines(root: Path, args: list[str]) -> list[str]:
    code, stdout, _stderr = run_git(root, args)
    if code != 0:
        return []
    return [line for line in stdout.splitlines() if line.strip()]


def detect_base(root: Path, explicit_base: str | None) -> str | None:
    if explicit_base:
        return explicit_base
    for candidate in ("origin/main", "origin/master", "main", "master"):
        code, _stdout, _stderr = run_git(root, ["rev-parse", "--verify", candidate])
        if code == 0:
            return candidate
    return None


def issue_refs(values: list[str]) -> list[str]:
    refs: set[str] = set()
    for value in values:
        for match in ISSUE_RE.finditer(value):
            refs.add(f"#{int(match.group(1))}")
    return sorted(refs, key=lambda item: int(item.lstrip("#")))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def inspect(root: Path, base_ref: str | None) -> dict[str, Any]:
    branch = run_git(root, ["branch", "--show-current"])[1] or None
    status = git_lines(root, ["status", "--short"])
    remotes = git_lines(root, ["remote", "-v"])
    base = detect_base(root, base_ref)

    commit_range = f"{base}..HEAD" if base else None
    commits = (
        git_lines(root, ["log", "--oneline", "--decorate=short", commit_range])
        if commit_range
        else []
    )
    changed_files = git_lines(root, ["diff", "--name-only", base]) if base else []
    tracking_docs = {
        path: {
            "exists": (root / path).is_file(),
            "changed_since_base": path in changed_files,
            "issue_refs": issue_refs([read_text(root / path)]),
        }
        for path in TRACKING_DOCS
    }
    all_issue_refs = issue_refs(commits + changed_files + [
        read_text(root / path) for path in TRACKING_DOCS
    ])

    return {
        "repository": str(root),
        "branch": branch,
        "base_ref": base,
        "remote": remotes,
        "working_tree_clean": not status,
        "status": status,
        "commits_since_base": commits,
        "changed_files_since_base": changed_files,
        "issue_refs": all_issue_refs,
        "tracking_docs": tracking_docs,
        "ready": bool(branch and base and commits and not status),
        "notes": [
            "remote actions still require explicit approval",
            "dirty working tree blocks PR creation unless the user requests proposal-only mode",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--base-ref")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    root = args.repository.resolve()
    if not root.is_dir():
        parser.error(f"repository does not exist: {root}")

    result = inspect(root, args.base_ref)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
