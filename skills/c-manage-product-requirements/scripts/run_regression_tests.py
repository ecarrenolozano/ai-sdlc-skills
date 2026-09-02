#!/usr/bin/env python3
"""Run deterministic regression tests for Product Requirements Management."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_scope_coverage.py"
TRACE_VALIDATOR = ROOT / "scripts" / "validate_trace_mutation.py"
ALIGNMENT_VALIDATOR = ROOT / "scripts" / "validate_workflow_alignment.py"
GOLDEN = ROOT / "references" / "golden-example"


def run(command: list[str]) -> tuple[int, dict[str, object] | str]:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    output = completed.stdout.strip() or completed.stderr.strip()
    try:
        payload: dict[str, object] | str = json.loads(output)
    except json.JSONDecodeError:
        payload = output
    return completed.returncode, payload


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validator(source: Path, requirements: Path, mode: str, sync: bool = True) -> tuple[int, dict[str, object] | str]:
    command = [sys.executable, str(VALIDATOR), str(source), str(requirements), "--mode", mode]
    if sync:
        command.append("--require-report-sync")
    return run(command)


def write_mutation(original: Path, transform) -> Path:
    text = original.read_text(encoding="utf-8")
    mutated = transform(text)
    handle = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    with handle:
        handle.write(mutated)
    return Path(handle.name)


def errors(payload: dict[str, object] | str) -> str:
    if isinstance(payload, dict):
        return "\n".join(str(item) for item in payload.get("errors", []))
    return str(payload)


def test_golden_examples() -> None:
    cases = [
        (
            GOLDEN / "initial-release" / "in-project-context.md",
            GOLDEN / "initial-release" / "out-product-requirements.md",
            "initial-release",
        ),
        (
            GOLDEN / "increment-broad-issue" / "in-triaged-issue.md",
            GOLDEN / "increment-broad-issue" / "out-product-requirements.md",
            "product-increment",
        ),
        (
            GOLDEN / "increment-user-story" / "in-triaged-issue.md",
            GOLDEN / "increment-user-story" / "out-product-requirements.md",
            "product-increment",
        ),
        (
            GOLDEN / "initial-release-umbrella" / "in-project-context.md",
            GOLDEN / "initial-release-umbrella" / "out-product-requirements-under-clarification.md",
            "initial-release",
        ),
    ]
    for source, requirements, mode in cases:
        code, payload = validator(source, requirements, mode, sync=True)
        require(code == 0, f"Golden example failed: {requirements}\n{payload}")
        require(isinstance(payload, dict) and payload.get("passed") is True, f"Golden result not passed: {requirements}")


def test_umbrella_fixture_has_no_umbrella_story() -> None:
    fixture = GOLDEN / "initial-release-umbrella" / "out-product-requirements-under-clarification.md"
    text = fixture.read_text(encoding="utf-8")
    require("US-0002 — Manage existing tasks" not in text, "Umbrella story remains in valid fixture.")
    require("Does \"manage tasks" not in text, "Redundant umbrella clarification remains in valid fixture.")
    require("| SRC-001 | Create and manage tasks on a personal board. |" in text, "Umbrella source statement is not registered.")
    require("| Umbrella | CAP-001, CAP-002, CAP-003, CAP-004 |" in text, "Umbrella decomposition is incomplete.")


def test_umbrella_capability_and_story_rejected() -> None:
    source = GOLDEN / "initial-release-umbrella" / "in-project-context.md"
    valid = GOLDEN / "initial-release-umbrella" / "out-product-requirements-under-clarification.md"

    def mutate(text: str) -> str:
        text = text.replace("Move a task between TODO, DOING, and DONE", "Manage existing tasks", 1)
        text = text.replace("### US-0002 — Move a task between board sections", "### US-0002 — Manage existing tasks")
        text = text.replace("I want to move a task between TODO, DOING, and DONE,", "I want to manage existing tasks,")
        return text

    path = write_mutation(valid, mutate)
    try:
        code, payload = validator(source, path, "initial-release", sync=True)
        detail = errors(payload)
        require(code == 1, f"Umbrella story was not rejected: {payload}")
        require("umbrella action" in detail.lower(), f"Umbrella rejection reason missing: {payload}")
    finally:
        path.unlink(missing_ok=True)


def test_source_omission_rejected() -> None:
    source = GOLDEN / "initial-release-umbrella" / "in-project-context.md"
    valid = GOLDEN / "initial-release-umbrella" / "out-product-requirements-under-clarification.md"

    def mutate(text: str) -> str:
        line = "| SRC-005 | Display basic task-status counts. | Project Context, Section 12, Included High-Level Capabilities | Atomic | CAP-006 | One independently observable outcome. |\n"
        return text.replace(line, "")

    path = write_mutation(valid, mutate)
    try:
        code, payload = validator(source, path, "initial-release", sync=True)
        detail = errors(payload)
        require(code == 1, f"Source omission was not rejected: {payload}")
        require("omitted from source register" in detail.lower(), f"Source omission reason missing: {payload}")
    finally:
        path.unlink(missing_ok=True)


def test_report_mismatch_rejected() -> None:
    source = GOLDEN / "initial-release-umbrella" / "in-project-context.md"
    valid = GOLDEN / "initial-release-umbrella" / "out-product-requirements-under-clarification.md"
    path = write_mutation(valid, lambda text: text.replace("**Scope coverage validator:** Preflight passed", "**Scope coverage validator:** Not run"))
    try:
        code, payload = validator(source, path, "initial-release", sync=True)
        detail = errors(payload)
        require(code == 1, f"Report mismatch was not rejected: {payload}")
        require("expected 'Preflight passed'" in detail, f"Report mismatch reason missing: {payload}")

        preflight_code, preflight_payload = validator(source, path, "initial-release", sync=False)
        require(preflight_code == 0, f"Unsynchronized preflight should calculate successfully: {preflight_payload}")
        require(
            isinstance(preflight_payload, dict)
            and preflight_payload["requirement_reports"][0]["expected"] == "Preflight passed",
            f"Preflight did not calculate expected status: {preflight_payload}",
        )
    finally:
        path.unlink(missing_ok=True)


def test_bidirectional_mapping_rejected() -> None:
    source = GOLDEN / "initial-release-umbrella" / "in-project-context.md"
    valid = GOLDEN / "initial-release-umbrella" / "out-product-requirements-under-clarification.md"
    path = write_mutation(valid, lambda text: text.replace("| CAP-002 | Move a task between TODO, DOING, and DONE | SRC-001, SRC-002 |", "| CAP-002 | Move a task between TODO, DOING, and DONE | SRC-002 |"))
    try:
        code, payload = validator(source, path, "initial-release", sync=True)
        detail = errors(payload)
        require(code == 1, f"Broken bidirectional mapping was not rejected: {payload}")
        require("does not map back" in detail.lower(), f"Bidirectional mapping reason missing: {payload}")
    finally:
        path.unlink(missing_ok=True)


def test_compound_story_rejected() -> None:
    source = GOLDEN / "initial-release-umbrella" / "in-project-context.md"
    valid = GOLDEN / "initial-release-umbrella" / "out-product-requirements-under-clarification.md"

    def mutate(text: str) -> str:
        text = text.replace("### US-0003 — Edit a task", "### US-0003 — Edit and delete a task")
        text = text.replace("I want to edit an existing task,", "I want to edit and delete an existing task,")
        return text

    path = write_mutation(valid, mutate)
    try:
        code, payload = validator(source, path, "initial-release", sync=True)
        detail = errors(payload)
        require(code == 1, f"Compound story was not rejected: {payload}")
        require("combines independent user actions" in detail.lower(), f"Compound story reason missing: {payload}")
    finally:
        path.unlink(missing_ok=True)



def test_observed_silent_behavior_fixture_rejected() -> None:
    source = GOLDEN / "initial-release-umbrella" / "in-project-context.md"
    invalid = ROOT / "references" / "test-fixtures" / "invalid-observed-umbrella-draft.md"
    code, payload = validator(source, invalid, "initial-release", sync=True)
    detail = errors(payload).lower()
    require(code == 1, f"Observed defective draft was accepted: {payload}")
    require("source statement coverage register" in detail, f"Missing source-register failure: {payload}")
    require("umbrella action" in detail, f"Missing umbrella-story failure: {payload}")
    require("expected 'failed'" in detail, f"Missing report-sync failure: {payload}")


def test_trace_mutation_guard() -> None:
    invalid_first_alias = "Run " + chr(98)
    invalid_second_alias = "Run " + chr(99)
    before = (
        "# Trace\n\n"
        "| Item | Type | Status | Current activity | Evidence | Missing or blocked | Next action |\n"
        "|---|---|---|---|---|---|---|\n"
        f"| Project request | Foundation | Complete | Request Clarification | request.md | None | {invalid_first_alias} |\n"
        f"| Initial requirements | Initial Release | Not Started | Product Requirements Management | context.md | Requirements missing | {invalid_second_alias} |\n"
    )
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        before_path = root / "before.md"
        allowed_path = root / "allowed.md"
        forbidden_path = root / "forbidden.md"
        before_path.write_text(before, encoding="utf-8")
        allowed_path.write_text(before.replace("| Initial requirements | Initial Release | Not Started |", "| Initial requirements | Initial Release | In Progress |"), encoding="utf-8")
        forbidden_path.write_text(before.replace("Request Clarification", "Silent unauthorized change"), encoding="utf-8")

        allowed_command = [
            sys.executable,
            str(TRACE_VALIDATOR),
            str(before_path),
            str(allowed_path),
            "--allow-field",
            "Initial requirements:Status",
        ]
        allowed_code, allowed_payload = run(allowed_command)
        require(allowed_code == 0, f"Authorized trace mutation was rejected: {allowed_payload}")

        forbidden_command = [
            sys.executable,
            str(TRACE_VALIDATOR),
            str(before_path),
            str(forbidden_path),
            "--allow-field",
            "Initial requirements:Status",
        ]
        forbidden_code, forbidden_payload = run(forbidden_command)
        require(forbidden_code == 1, f"Unauthorized trace mutation was accepted: {forbidden_payload}")


def test_workflow_alignment() -> None:
    code, payload = run([
        sys.executable,
        str(ALIGNMENT_VALIDATOR),
        str(ROOT / "SKILL.md"),
        str(ROOT / "references" / "process-flowchart.md"),
    ])
    require(code == 0, f"Workflow alignment failed: {payload}")
    require(isinstance(payload, dict) and payload.get("passed") is True, f"Alignment did not pass: {payload}")
    require(payload.get("workflow_steps") == list(range(1, 77)), f"Workflow is not exactly 1-76: {payload}")


def main() -> int:
    tests = [
        test_golden_examples,
        test_umbrella_fixture_has_no_umbrella_story,
        test_umbrella_capability_and_story_rejected,
        test_source_omission_rejected,
        test_report_mismatch_rejected,
        test_bidirectional_mapping_rejected,
        test_compound_story_rejected,
        test_observed_silent_behavior_fixture_rejected,
        test_trace_mutation_guard,
        test_workflow_alignment,
    ]
    results: list[dict[str, str]] = []
    for test in tests:
        try:
            test()
            results.append({"test": test.__name__, "result": "passed"})
        except Exception as exc:
            results.append({"test": test.__name__, "result": "failed", "error": str(exc)})
            print(json.dumps({"passed": False, "results": results}, indent=2, ensure_ascii=False))
            return 1
    print(json.dumps({"passed": True, "tests": len(tests), "results": results}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
