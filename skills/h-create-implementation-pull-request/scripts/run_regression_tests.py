#!/usr/bin/env python3
"""Regression checks for h-create-implementation-pull-request."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
INSPECTOR = SKILL_ROOT / "scripts/inspect_pr_readiness.py"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(command: list[str], cwd: Path, *, expected: int | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True, timeout=30)
    if expected is not None:
        check(result.returncode == expected, f"unexpected exit {result.returncode}: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    return result


def create_git_repo(root: Path) -> None:
    run(["git", "init", "-b", "main"], root, expected=0)
    run(["git", "config", "user.email", "test@example.com"], root, expected=0)
    run(["git", "config", "user.name", "Test User"], root, expected=0)
    (root / "sdlc_docs/03_implementation").mkdir(parents=True)
    (root / "sdlc_docs/trace_workflow.md").write_text(
        "# Workflow Traceability\n\n| Item | Type | Status |\n|---|---|---|\n| Implementation | Initial Release | In Progress |\n",
        encoding="utf-8",
    )
    (root / "sdlc_docs/03_implementation/backlog_priority.md").write_text(
        "# Backlog Priority Guidance\n\n#1 implemented locally\n#5 implemented locally\n",
        encoding="utf-8",
    )
    (root / "src").mkdir()
    (root / "src/app.py").write_text("VALUE = 1\n", encoding="utf-8")
    run(["git", "add", "."], root, expected=0)
    run(["git", "commit", "-m", "Initial"], root, expected=0)
    run(["git", "checkout", "-b", "feature/issues-1-5"], root, expected=0)
    (root / "src/app.py").write_text("VALUE = 2\n", encoding="utf-8")
    run(["git", "add", "."], root, expected=0)
    run(["git", "commit", "-m", "Implement #1 and #5"], root, expected=0)


def main() -> int:
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    checks: list[tuple[str, bool]] = []
    checks.append(("frontmatter name", "name: h-create-implementation-pull-request" in skill_text))
    checks.append(("approval boundary", "explicit approval" in skill_text and "gh pr create" in skill_text))
    checks.append(("no auto close keywords", "auto-close keywords" in skill_text and "unless the user explicitly approves" in skill_text))
    checks.append(("grouping policy", "one PR per coherent implementation batch" in skill_text))
    checks.append(("status tracking", "sdlc_docs/trace_workflow.md" in skill_text and "sdlc_docs/03_implementation/backlog_priority.md" in skill_text))
    checks.append(("no implementation", "Do not implement product code" in skill_text))
    checks.append(("references exist", (SKILL_ROOT / "references/pr-policy.md").is_file() and (SKILL_ROOT / "references/proposal-and-result-patterns.md").is_file()))

    compile(INSPECTOR.read_text(encoding="utf-8"), str(INSPECTOR), "exec")
    checks.append(("inspector compiles", True))

    with tempfile.TemporaryDirectory() as temporary:
        repo = Path(temporary)
        create_git_repo(repo)
        inspected = run([sys.executable, str(INSPECTOR), str(repo), "--base-ref", "main"], repo, expected=0)
        payload = json.loads(inspected.stdout)
        checks.append(("inspector ready", payload["ready"] is True))
        checks.append(("inspector branch", payload["branch"] == "feature/issues-1-5"))
        checks.append(("inspector issue refs", "#1" in payload["issue_refs"] and "#5" in payload["issue_refs"]))
        checks.append(("inspector tracking docs", payload["tracking_docs"]["sdlc_docs/trace_workflow.md"]["exists"] is True))

        (repo / "src/dirty.py").write_text("DIRTY = True\n", encoding="utf-8")
        dirty = run([sys.executable, str(INSPECTOR), str(repo), "--base-ref", "main"], repo, expected=1)
        checks.append(("dirty tree blocks ready", json.loads(dirty.stdout)["ready"] is False))

    for name, condition in checks:
        check(condition, name)
        print(f"PASS: {name}")
    print(f"PASS: {len(checks)} regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
