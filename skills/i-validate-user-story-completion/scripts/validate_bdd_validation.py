#!/usr/bin/env python3
"""Validate BDD user-story completion artifacts for a repository."""
from __future__ import annotations

import argparse
import ast
import json
import re
import tomllib
from pathlib import Path
from typing import Any


TRACE_ROW_RE = re.compile(r"^\|\s*User story validation\s*\|", re.MULTILINE)
FEATURE_RE = re.compile(r"^\s*Feature:\s+\S+", re.MULTILINE)
SCENARIO_RE = re.compile(r"^\s*Scenario(?: Outline)?:\s+\S+", re.MULTILINE)
GIVEN_RE = re.compile(r"^\s*(?:Given|And)\s+\S+", re.MULTILINE)
WHEN_RE = re.compile(r"^\s*When\s+\S+", re.MULTILINE)
THEN_RE = re.compile(r"^\s*Then\s+\S+", re.MULTILINE)
SKIP_RE = re.compile(r"pytest\.mark\.(?:skip|skipif|xfail)|@pytest\.(?:mark\.)?(?:skip|skipif|xfail)")


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
    return match.group(1).casefold() if match else None


def dependencies(pyproject: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    project = pyproject.get("project")
    if isinstance(project, dict):
        for value in project.get("dependencies", []) or []:
            if name := requirement_name(value):
                result.add(name)
    groups = pyproject.get("dependency-groups")
    if isinstance(groups, dict):
        for values in groups.values():
            if isinstance(values, list):
                for value in values:
                    if name := requirement_name(value):
                        result.add(name)
    return result


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


def validate(root: Path, stories: list[str], require_trace: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    root = root.resolve()

    pyproject = load_pyproject(root / "pyproject.toml")
    deps = dependencies(pyproject)
    if "pytest" not in deps:
        errors.append("pytest is not declared")
    if "pytest-bdd" not in deps:
        errors.append("pytest-bdd is not declared")

    features_dir = root / "tests" / "validation" / "features"
    steps_dir = root / "tests" / "validation" / "steps"
    if not features_dir.is_dir():
        errors.append("missing tests/validation/features")
    if not steps_dir.is_dir():
        errors.append("missing tests/validation/steps")

    feature_files = sorted(features_dir.glob("*.feature")) if features_dir.is_dir() else []
    step_files = sorted(steps_dir.rglob("test_*.py")) if steps_dir.is_dir() else []
    if not feature_files:
        errors.append("no Gherkin feature files found")
    if not step_files:
        errors.append("no pytest-bdd step modules found")

    feature_text = ""
    for path in feature_files:
        text = path.read_text(encoding="utf-8")
        feature_text += "\n" + text
        if not FEATURE_RE.search(text):
            errors.append(f"feature file missing Feature header: {path.relative_to(root)}")
        if not SCENARIO_RE.search(text):
            errors.append(f"feature file missing Scenario: {path.relative_to(root)}")
        if not GIVEN_RE.search(text) or not WHEN_RE.search(text) or not THEN_RE.search(text):
            errors.append(f"feature file missing Given/When/Then coverage: {path.relative_to(root)}")

    step_text = ""
    for path in step_files:
        text = path.read_text(encoding="utf-8")
        step_text += "\n" + text
        if "pytest_bdd" not in text:
            errors.append(f"step module does not import/use pytest_bdd: {path.relative_to(root)}")
        if SKIP_RE.search(text):
            errors.append(f"step module hides validation with skip or xfail: {path.relative_to(root)}")
        if has_unittest_testcase(path):
            errors.append(f"unittest.TestCase is not allowed: {path.relative_to(root)}")

    for story in stories:
        if story and story not in feature_text and story not in step_text:
            warnings.append(f"story identifier not found in validation artifacts: {story}")

    trace = root / "sdlc_docs" / "trace_workflow.md"
    trace_present = trace.is_file()
    trace_has_row = False
    if trace_present:
        trace_has_row = TRACE_ROW_RE.search(trace.read_text(encoding="utf-8")) is not None
    if require_trace and not trace_present:
        errors.append("sdlc_docs/trace_workflow.md is required but missing")
    if require_trace and trace_present and not trace_has_row:
        errors.append("trace_workflow.md is missing User story validation row")

    return {
        "passed": not errors,
        "repository": str(root),
        "stories": stories,
        "feature_files": [str(path.relative_to(root)) for path in feature_files],
        "step_files": [str(path.relative_to(root)) for path in step_files],
        "trace_workflow": {
            "exists": trace_present,
            "user_story_validation_row": trace_has_row,
        },
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", type=Path)
    parser.add_argument("--story", action="append", default=[])
    parser.add_argument("--require-trace", action="store_true")
    args = parser.parse_args()

    result = validate(args.repository, args.story, args.require_trace)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
