#!/usr/bin/env python3
"""Validate essential technical-foundation conditions without enforcing style trivia."""
from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path
from typing import Any

REQUIRED_TEST_DIRS = (
    "tests/unit",
    "tests/integration",
    "tests/regression",
    "tests/validation",
    "tests/validation/features",
    "tests/validation/steps",
)
REQUIRED_DOCS = ("README.md", "tests/README.md", "docs/development.md")
GENERATED_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".structurizr",
}
IGNORED_GENERATED_PARTS = {
    ".git",
    ".venv",
    "dist",
    "build",
    "site",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def load_pyproject(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def requirement_name(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    match = re.match(r"\s*([A-Za-z0-9_.-]+)", value)
    return match.group(1).lower() if match else None


def dependency_names(pyproject: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    project = pyproject.get("project")
    if isinstance(project, dict):
        for value in project.get("dependencies", []):
            if name := requirement_name(value):
                result.add(name)
        optional = project.get("optional-dependencies", {})
        if isinstance(optional, dict):
            for values in optional.values():
                if isinstance(values, list):
                    for value in values:
                        if name := requirement_name(value):
                            result.add(name)
    groups = pyproject.get("dependency-groups", {})
    if isinstance(groups, dict):
        for values in groups.values():
            if isinstance(values, list):
                for value in values:
                    if name := requirement_name(value):
                        result.add(name)
    return result


def workflow_files(root: Path) -> list[Path]:
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return []
    return sorted([*directory.glob("*.yml"), *directory.glob("*.yaml")])


def has_checkout_documentation(root: Path) -> bool:
    text = "\n".join(read_text(root / path) for path in REQUIRED_DOCS).lower()
    checkout = "repository checkout" in text or "checkout-based" in text
    package_scope = "python package" in text and "uv build" in text
    return checkout and package_scope


def validate_repository(root: Path) -> dict[str, object]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.is_file():
        errors.append("missing_pyproject")
        pyproject: dict[str, Any] = {}
    else:
        pyproject = load_pyproject(pyproject_path)
        if not pyproject:
            errors.append("invalid_pyproject")

    dependencies = dependency_names(pyproject)
    if "pytest" not in dependencies:
        errors.append("pytest_not_declared")
    if "pytest-bdd" not in dependencies:
        errors.append("pytest_bdd_not_declared")

    pytest_config = pyproject.get("tool", {}).get("pytest", {}).get("ini_options", {}) if pyproject else {}
    if not isinstance(pytest_config, dict):
        pytest_config = {}
    testpaths = pytest_config.get("testpaths", [])
    if isinstance(testpaths, str):
        testpaths = [testpaths]
    if "tests" not in testpaths:
        errors.append("pytest_testpaths_missing")

    markers = pytest_config.get("markers", [])
    marker_text = "\n".join(markers) if isinstance(markers, list) else ""
    for marker in ("unit", "integration", "regression", "validation"):
        if not re.search(rf"(^|\n)\s*{marker}\s*:", marker_text):
            warnings.append(f"pytest_marker_not_registered:{marker}")

    for relative in REQUIRED_TEST_DIRS:
        if not (root / relative).is_dir():
            errors.append(f"missing_test_directory:{relative}")

    active_test_files = sorted((root / "tests").rglob("*.py")) if (root / "tests").is_dir() else []
    for path in active_test_files:
        text = read_text(path)
        if re.search(r"\bunittest\.TestCase\b|\bfrom\s+unittest\s+import\s+TestCase\b", text):
            errors.append(f"unittest_testcase:{path.relative_to(root)}")

    smoke_tests = [
        path
        for base in (root / "tests" / "unit", root / "tests" / "integration")
        if base.is_dir()
        for path in base.rglob("test_*.py")
    ]
    if not smoke_tests:
        errors.append("technical_smoke_tests_missing")

    for relative in REQUIRED_DOCS:
        if not (root / relative).is_file():
            errors.append(f"missing_documentation:{relative}")

    workflows = workflow_files(root)
    if not workflows:
        errors.append("ci_workflow_missing")
    elif (root / "uv.lock").is_file():
        workflow_text = "\n".join(read_text(path) for path in workflows)
        unlocked = re.search(r"uv\s+sync\s+--all-groups(?![^\n]*--locked)", workflow_text)
        locked = re.search(r"uv\s+sync[^\n]*--locked[^\n]*--all-groups|uv\s+sync[^\n]*--all-groups[^\n]*--locked", workflow_text)
        if unlocked:
            errors.append("ci_uses_unlocked_uv_sync")
        if not locked:
            errors.append("ci_missing_locked_uv_sync")

    generated: list[str] = []
    for path in root.rglob("*"):
        relative_parts = path.relative_to(root).parts
        if any(part in IGNORED_GENERATED_PARTS for part in relative_parts):
            continue
        if path.name in GENERATED_NAMES or path.suffix in {".pyc", ".pyo"}:
            generated.append(str(path.relative_to(root)))
    if generated:
        errors.append("generated_artifacts_present")

    frontend = root / "frontend"
    wheel = pyproject.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel", {}) if pyproject else {}
    packages = wheel.get("packages", []) if isinstance(wheel, dict) else []
    frontend_packaged = any("frontend" in str(item).lower() for item in packages) if isinstance(packages, list) else False
    if frontend.is_dir() and packages and not frontend_packaged and not has_checkout_documentation(root):
        errors.append("checkout_execution_not_documented")

    return {
        "passed": not errors,
        "repository": str(root),
        "errors": errors,
        "warnings": warnings,
        "details": {
            "dependencies": sorted(dependencies),
            "workflow_files": [str(path.relative_to(root)) for path in workflows],
            "smoke_tests": [str(path.relative_to(root)) for path in smoke_tests],
            "generated_artifacts": generated,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    result = validate_repository(args.repository)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
