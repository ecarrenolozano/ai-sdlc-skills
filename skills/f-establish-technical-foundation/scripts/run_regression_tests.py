#!/usr/bin/env python3
"""Run focused regression checks for the simplified foundation skill."""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_ROOT = SKILL_ROOT / "references" / "golden-example" / "browser-task-board"
VALIDATOR_PATH = SKILL_ROOT / "scripts" / "validate_foundation.py"
INSPECTOR_PATH = SKILL_ROOT / "scripts" / "inspect_technical_foundation.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("foundation_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load validate_foundation.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


def copy_golden_output() -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary = tempfile.TemporaryDirectory(prefix="foundation-regression-")
    target = Path(temporary.name) / "repository"
    shutil.copytree(GOLDEN_ROOT / "out-repository", target)
    return temporary, target


def assert_error(result: dict[str, object], expected: str) -> None:
    errors = result.get("errors", [])
    if expected not in errors:
        raise AssertionError(f"Expected {expected!r}, got {errors!r}")


def test_golden_output_passes() -> None:
    result = VALIDATOR.validate_repository(GOLDEN_ROOT / "out-repository")
    if not result["passed"]:
        raise AssertionError(json.dumps(result, indent=2))


def test_missing_pyproject_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        (target / "pyproject.toml").unlink()
        assert_error(VALIDATOR.validate_repository(target), "missing_pyproject")
    finally:
        temporary.cleanup()


def test_missing_pytest_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        path = target / "pyproject.toml"
        path.write_text(path.read_text().replace('  "pytest>=8.4,<9",\n', ""), encoding="utf-8")
        assert_error(VALIDATOR.validate_repository(target), "pytest_not_declared")
    finally:
        temporary.cleanup()


def test_missing_pytest_bdd_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        path = target / "pyproject.toml"
        path.write_text(path.read_text().replace('  "pytest-bdd>=8,<9",\n', ""), encoding="utf-8")
        assert_error(VALIDATOR.validate_repository(target), "pytest_bdd_not_declared")
    finally:
        temporary.cleanup()


def test_missing_test_directory_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        shutil.rmtree(target / "tests" / "integration")
        assert_error(
            VALIDATOR.validate_repository(target),
            "missing_test_directory:tests/integration",
        )
    finally:
        temporary.cleanup()


def test_unittest_testcase_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        path = target / "tests" / "unit" / "test_unittest_style.py"
        path.write_text("import unittest\n\nclass TestThing(unittest.TestCase):\n    pass\n", encoding="utf-8")
        result = VALIDATOR.validate_repository(target)
        if not any(str(item).startswith("unittest_testcase:") for item in result["errors"]):
            raise AssertionError(result)
    finally:
        temporary.cleanup()


def test_unlocked_ci_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        workflow = target / ".github" / "workflows" / "quality.yml"
        workflow.write_text(workflow.read_text().replace("uv sync --locked --all-groups", "uv sync --all-groups"), encoding="utf-8")
        assert_error(VALIDATOR.validate_repository(target), "ci_uses_unlocked_uv_sync")
    finally:
        temporary.cleanup()


def test_missing_documentation_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        (target / "docs" / "development.md").unlink()
        assert_error(
            VALIDATOR.validate_repository(target),
            "missing_documentation:docs/development.md",
        )
    finally:
        temporary.cleanup()


def test_missing_smoke_tests_fails() -> None:
    temporary, target = copy_golden_output()
    try:
        for base in (target / "tests" / "unit", target / "tests" / "integration"):
            for path in base.rglob("test_*.py"):
                path.unlink()
        assert_error(VALIDATOR.validate_repository(target), "technical_smoke_tests_missing")
    finally:
        temporary.cleanup()


def test_checkout_documentation_required() -> None:
    temporary, target = copy_golden_output()
    try:
        for relative in ("README.md", "docs/development.md", "tests/README.md"):
            path = target / relative
            text = path.read_text(encoding="utf-8")
            text = text.replace("repository checkout", "working tree")
            text = text.replace("Python package", "package")
            text = text.replace("python package", "package")
            path.write_text(text, encoding="utf-8")
        assert_error(VALIDATOR.validate_repository(target), "checkout_execution_not_documented")
    finally:
        temporary.cleanup()


def test_inspector_is_read_only_and_toml_based() -> None:
    temporary, target = copy_golden_output()
    try:
        before = sorted(str(path.relative_to(target)) for path in target.rglob("*"))
        completed = subprocess.run(
            [sys.executable, str(INSPECTOR_PATH), str(target)],
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(completed.stderr or completed.stdout)
        payload = json.loads(completed.stdout)
        detected = set(payload["dependencies_detected"])
        if "pytest" not in detected or "pytest-bdd" not in detected or "Edwin" in detected:
            raise AssertionError(payload)
        after = sorted(str(path.relative_to(target)) for path in target.rglob("*"))
        if before != after:
            raise AssertionError("Inspector modified repository contents")
    finally:
        temporary.cleanup()


def test_workflow_matches_flowchart() -> None:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    flow_text = (SKILL_ROOT / "references" / "process-flowchart.md").read_text(encoding="utf-8")
    for number in range(1, 19):
        if f"{number}. " not in skill_text:
            raise AssertionError(f"Missing workflow step {number}")
        if f"{number}. " not in flow_text:
            raise AssertionError(f"Missing flowchart step {number}")


def test_golden_contains_no_product_implementation() -> None:
    source = GOLDEN_ROOT / "out-repository" / "src"
    text = "\n".join(path.read_text(encoding="utf-8") for path in source.rglob("*.py"))
    forbidden = ("create_task", "move_task", "delete_task", "edit_task", "/api/tasks")
    present = [term for term in forbidden if term in text]
    if present:
        raise AssertionError(f"Golden example contains product behavior: {present}")


def main() -> int:
    tests = [
        test_golden_output_passes,
        test_missing_pyproject_fails,
        test_missing_pytest_fails,
        test_missing_pytest_bdd_fails,
        test_missing_test_directory_fails,
        test_unittest_testcase_fails,
        test_unlocked_ci_fails,
        test_missing_documentation_fails,
        test_missing_smoke_tests_fails,
        test_checkout_documentation_required,
        test_inspector_is_read_only_and_toml_based,
        test_workflow_matches_flowchart,
        test_golden_contains_no_product_implementation,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as exc:  # noqa: BLE001 - regression runner reports every failure
            failures.append(f"{test.__name__}: {exc}")
            print(f"FAIL {test.__name__}: {exc}")
        else:
            print(f"PASS {test.__name__}")
    print(f"\n{len(tests) - len(failures)}/{len(tests)} checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
