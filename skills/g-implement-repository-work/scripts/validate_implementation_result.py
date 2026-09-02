#!/usr/bin/env python3
"""Run objective post-implementation checks for one local repository issue."""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import tomllib
from pathlib import Path
from typing import Any


TEST_ROOTS = (
    "tests/unit/",
    "tests/integration/",
    "tests/regression/",
    "tests/validation/",
)
PRODUCTION_PREFIXES = ("src/", "frontend/")
CODE_LEVEL_DOCUMENT = "sdlc_docs/02_architecture/code-level.md"
TRACE_WORKFLOW_DOCUMENT = "sdlc_docs/trace_workflow.md"
BACKLOG_PRIORITY_DOCUMENT = "sdlc_docs/03_implementation/backlog_priority.md"
CODE_LEVEL_CONTAINER_RE = re.compile(r"^sdlc_docs/02_architecture/containers/[^/]+/code-level\.md$")
MERMAID_RE = re.compile(r"```mermaid\s+(sequenceDiagram|flowchart|classDiagram)", re.MULTILINE)
IMPLEMENTATION_ROW_RE = re.compile(r"^\|\s*Implementation\s*\|", re.MULTILINE)
SKIP_PATTERNS = (
    re.compile(r"pytest\.mark\.(?:skip|skipif|xfail)"),
    re.compile(r"@pytest\.(?:mark\.)?(?:skip|skipif|xfail)"),
)


def dependency_names(pyproject: Path) -> set[str]:
    if not pyproject.exists():
        return set()
    try:
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return set()
    raw: list[str] = []
    raw.extend((data.get("project", {}) or {}).get("dependencies", []) or [])
    for group in (data.get("dependency-groups", {}) or {}).values():
        if isinstance(group, list):
            raw.extend(group)
    names: set[str] = set()
    for value in raw:
        if not isinstance(value, str):
            continue
        match = re.match(r"[A-Za-z0-9_.-]+", value)
        if match:
            names.add(match.group(0).casefold())
    return names


def derive_changed_files(root: Path, base_ref: str | None) -> list[str]:
    if not (root / ".git").exists():
        return []
    command = ["git", "diff", "--name-only"]
    if base_ref:
        command.append(base_ref)
    try:
        result = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def has_unittest_testcase(path: Path) -> bool:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError):
        return False
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            if isinstance(base, ast.Attribute) and base.attr == "TestCase":
                return True
            if isinstance(base, ast.Name) and base.id == "TestCase":
                return True
    return False


def validate(root: Path, issue: str, work_type: str, changed_files: list[str]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    dependencies = dependency_names(root / "pyproject.toml")

    if not issue.strip():
        errors.append("an explicit issue or work item is required")
    if "pytest" not in dependencies:
        errors.append("pytest is not declared in pyproject.toml")

    for directory in ("unit", "integration", "regression", "validation"):
        if not (root / "tests" / directory).is_dir():
            errors.append(f"missing tests/{directory}/")

    test_files = sorted((root / "tests").rglob("*.py")) if (root / "tests").exists() else []
    for path in test_files:
        if has_unittest_testcase(path):
            errors.append(f"unittest.TestCase is not allowed for new project tests: {path.relative_to(root)}")

    normalized = [path.replace("\\", "/").lstrip("./") for path in changed_files]
    production_changed = [path for path in normalized if path.startswith(PRODUCTION_PREFIXES)]
    tests_changed = [path for path in normalized if path.startswith(TEST_ROOTS) and path.endswith(".py")]
    code_level_changed_files = [
        path for path in normalized
        if path == CODE_LEVEL_DOCUMENT or CODE_LEVEL_CONTAINER_RE.match(path)
    ]
    code_level_changed = bool(code_level_changed_files)
    code_level_exists = (root / CODE_LEVEL_DOCUMENT).is_file()
    trace_workflow_path = root / TRACE_WORKFLOW_DOCUMENT
    trace_workflow_exists = trace_workflow_path.is_file()
    trace_workflow_changed = TRACE_WORKFLOW_DOCUMENT in normalized
    trace_workflow_text = trace_workflow_path.read_text(encoding="utf-8") if trace_workflow_exists else ""
    trace_workflow_has_implementation = IMPLEMENTATION_ROW_RE.search(trace_workflow_text) is not None
    backlog_priority_path = root / BACKLOG_PRIORITY_DOCUMENT
    backlog_priority_exists = backlog_priority_path.is_file()
    backlog_priority_changed = BACKLOG_PRIORITY_DOCUMENT in normalized
    per_container_code_level = sorted(
        str(path.relative_to(root)).replace("\\", "/")
        for path in (root / "sdlc_docs/02_architecture/containers").glob("*/code-level.md")
    ) if (root / "sdlc_docs/02_architecture/containers").is_dir() else []

    if work_type in {"story", "bug"} and production_changed and not tests_changed:
        errors.append("production behavior changed without a changed pytest module")

    if production_changed and not (code_level_exists or per_container_code_level):
        errors.append("production code changed without central or per-container code-level architecture docs")

    if production_changed and (code_level_exists or per_container_code_level) and not code_level_changed:
        warnings.append("production code changed without updating code-level architecture docs; verify they were already current")

    if production_changed and not trace_workflow_exists:
        warnings.append("production code changed but sdlc_docs/trace_workflow.md is missing; implementation traceability cannot be verified")
    elif production_changed and not trace_workflow_changed:
        warnings.append("production code changed without updating sdlc_docs/trace_workflow.md; verify the Implementation row was already current")
    elif production_changed and not trace_workflow_has_implementation:
        errors.append("sdlc_docs/trace_workflow.md changed but no Implementation row was found")

    if production_changed and backlog_priority_exists and not backlog_priority_changed:
        warnings.append("production code changed without updating sdlc_docs/03_implementation/backlog_priority.md; verify implementation status and next priority were already current")

    changed_code_level_text = ""
    for relative in code_level_changed_files:
        path = root / relative
        if path.exists():
            changed_code_level_text += "\n" + path.read_text(encoding="utf-8")
    if production_changed and code_level_changed and not MERMAID_RE.search(changed_code_level_text):
        warnings.append("code-level architecture docs changed without Mermaid diagrams; verify the change was trivial or diagrams were not useful")

    if work_type == "bug" and not any(path.startswith("tests/regression/") for path in tests_changed):
        errors.append("bug work requires a changed regression test under tests/regression/")

    for relative in tests_changed:
        path = root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in SKIP_PATTERNS):
            errors.append(f"changed test hides behavior with skip or xfail: {relative}")

    governance_changes = [
        path for path in normalized
        if path.startswith(("sdlc_docs/00_inception/", "sdlc_docs/01_requirements/", "sdlc_docs/02_architecture/"))
        and path != CODE_LEVEL_DOCUMENT
        and not CODE_LEVEL_CONTAINER_RE.match(path)
    ]
    if governance_changes:
        warnings.append("approved context, requirements, or architecture files changed; verify separate approval")

    if not normalized:
        warnings.append("changed files unavailable; Git metadata or --changed-file values were not provided")

    return {
        "issue": issue,
        "work_type": work_type,
        "changed_files": normalized,
        "production_files_changed": production_changed,
        "test_files_changed": tests_changed,
        "code_level_document": {
            "path": CODE_LEVEL_DOCUMENT,
            "exists": code_level_exists,
            "changed": code_level_changed,
            "changed_files": code_level_changed_files,
            "per_container": per_container_code_level,
        },
        "workflow_traceability": {
            "path": TRACE_WORKFLOW_DOCUMENT,
            "exists": trace_workflow_exists,
            "changed": trace_workflow_changed,
            "implementation_row_present": trace_workflow_has_implementation,
        },
        "local_status_tracking": {
            "trace_workflow": {
                "path": TRACE_WORKFLOW_DOCUMENT,
                "exists": trace_workflow_exists,
                "changed": trace_workflow_changed,
                "implementation_row_present": trace_workflow_has_implementation,
            },
            "backlog_priority": {
                "path": BACKLOG_PRIORITY_DOCUMENT,
                "exists": backlog_priority_exists,
                "changed": backlog_priority_changed,
            },
        },
        "errors": errors,
        "warnings": warnings,
        "valid": not errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", type=Path)
    parser.add_argument("--issue", required=True)
    parser.add_argument(
        "--work-type",
        choices=("story", "bug", "refactor", "documentation"),
        default="story",
    )
    parser.add_argument("--base-ref")
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    root = args.repository.resolve()
    if not root.is_dir():
        parser.error(f"repository does not exist: {root}")

    changed_files = args.changed_file or derive_changed_files(root, args.base_ref)
    result = validate(root, args.issue, args.work_type, changed_files)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
