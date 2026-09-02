#!/usr/bin/env python3
"""Inspect repository readiness for implementation planning or one issue implementation."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tomllib
from pathlib import Path
from typing import Any


CANONICAL_FILES = (
    "sdlc_docs/01_requirements/product_requirements.md",
    "sdlc_docs/02_architecture/architecture.md",
    "sdlc_docs/trace_workflow.md",
    "pyproject.toml",
)

SKILL_ROOT = Path(__file__).resolve().parents[1]
BEST_PRACTICES_DIR = SKILL_ROOT / "references" / "best-practices"
IMPLEMENTATION_DIR = "sdlc_docs/03_implementation"
BACKLOG_PRIORITY_DOC = "sdlc_docs/03_implementation/backlog_priority.md"
CODE_LEVEL_INDEX = "sdlc_docs/02_architecture/code-level.md"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def trace_status(trace_text: str, item_name: str) -> str | None:
    target = item_name.casefold()
    for line in trace_text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0].casefold() == target:
            return cells[2]
    return None


def dependency_names(pyproject: Path) -> list[str]:
    if not pyproject.exists():
        return []
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return []

    values: list[str] = []
    project = data.get("project", {})
    values.extend(project.get("dependencies", []) or [])
    for dependencies in (data.get("dependency-groups", {}) or {}).values():
        if isinstance(dependencies, list):
            values.extend(dependencies)

    names = []
    for value in values:
        if not isinstance(value, str):
            continue
        name = value.split(";", 1)[0].strip()
        for token in ("[", "<", ">", "=", "!", "~", " "):
            name = name.split(token, 1)[0]
        if name:
            names.append(name.casefold())
    return sorted(set(names))


def git_state(root: Path) -> dict[str, Any]:
    if not (root / ".git").exists():
        return {"available": False, "branch": None, "status": []}
    try:
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        status_output = subprocess.run(
            ["git", "status", "--short"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return {"available": True, "branch": None, "status": [], "error": "git inspection failed"}
    return {
        "available": True,
        "branch": branch or None,
        "status": [line for line in status_output.splitlines() if line.strip()],
    }


def best_practice_references() -> list[str]:
    if not BEST_PRACTICES_DIR.is_dir():
        return []
    return sorted(
        str(path.relative_to(SKILL_ROOT))
        for path in BEST_PRACTICES_DIR.glob("*.md")
    )


def per_container_code_level_documents(root: Path) -> dict[str, bool]:
    containers_root = root / "sdlc_docs/02_architecture/containers"
    if not containers_root.is_dir():
        return {}
    return {
        str(path.relative_to(root)).replace("\\", "/"): (path / "code-level.md").is_file()
        for path in sorted(containers_root.iterdir())
        if path.is_dir()
    }


def inspect(root: Path, issue: str | None, mode: str) -> dict[str, Any]:
    trace = read_text(root / "sdlc_docs/trace_workflow.md")
    dependencies = dependency_names(root / "pyproject.toml")
    tests_root = root / "tests"

    result: dict[str, Any] = {
        "repository": str(root),
        "mode": mode,
        "selected_issue": issue,
        "canonical_files": {
            path: (root / path).exists() for path in CANONICAL_FILES
        },
        "workflow_status": {
            "Architecture": trace_status(trace, "Architecture"),
            "Repository preparation": trace_status(trace, "Repository preparation"),
            "Technical foundation": trace_status(trace, "Technical foundation"),
            "Implementation": trace_status(trace, "Implementation"),
        },
        "test_directories": {
            name: (tests_root / name).is_dir()
            for name in ("unit", "integration", "regression", "validation")
        },
        "pytest_available": "pytest" in dependencies,
        "pytest_bdd_available": "pytest-bdd" in dependencies,
        "implementation_documents": {
            "directory": (root / IMPLEMENTATION_DIR).is_dir(),
            "readme": (root / IMPLEMENTATION_DIR / "README.md").is_file(),
            "backlog_priority": (root / BACKLOG_PRIORITY_DOC).is_file(),
        },
        "code_level_documents": {
            "central_index": (root / CODE_LEVEL_INDEX).is_file(),
            "per_container": per_container_code_level_documents(root),
        },
        "best_practice_references": best_practice_references(),
        "multi_agent_support": shutil.which("codex") is not None,
        "ping_pong_tdd_fallback": "simulate tester and developer roles when subagents are unavailable",
        "git": git_state(root),
    }

    base_ready = bool(
        all(result["canonical_files"].values())
        and result["workflow_status"]["Architecture"] == "Complete"
        and result["workflow_status"]["Repository preparation"] == "Complete"
        and result["workflow_status"]["Technical foundation"] == "Complete"
    )
    implementation_ready = bool(
        base_ready
        and issue
        and all(result["test_directories"].values())
        and result["pytest_available"]
    )
    planning_ready = bool(base_ready)
    result["ready"] = planning_ready if mode == "backlog-priority" else implementation_ready
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument(
        "--mode",
        choices=("single-issue", "backlog-priority"),
        default="single-issue",
        help="Readiness mode to inspect",
    )
    parser.add_argument("--issue", help="Explicit selected issue or approved work item")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    root = args.repository.resolve()
    if not root.is_dir():
        parser.error(f"repository does not exist: {root}")

    result = inspect(root, args.issue, args.mode)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
