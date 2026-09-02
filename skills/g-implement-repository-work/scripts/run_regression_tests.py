#!/usr/bin/env python3
"""Regression checks for g-implement-repository-work."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
FLOWCHART = SKILL_ROOT / "references/process-flowchart.md"
INSPECTOR = SKILL_ROOT / "scripts/inspect_implementation_readiness.py"
VALIDATOR = SKILL_ROOT / "scripts/validate_implementation_result.py"
GOLDEN = SKILL_ROOT / "references/golden-example/browser-task-board"


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(command: list[str], *, expected: int | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=30)
    if expected is not None:
        check(result.returncode == expected, f"unexpected exit {result.returncode}: {' '.join(command)}\n{result.stdout}\n{result.stderr}")
    return result


def create_repo(root: Path, foundation_status: str = "Complete") -> None:
    (root / "sdlc_docs/01_requirements").mkdir(parents=True)
    (root / "sdlc_docs/02_architecture").mkdir(parents=True)
    (root / "sdlc_docs/02_architecture/containers/flask-backend").mkdir(parents=True)
    (root / "sdlc_docs/03_implementation").mkdir(parents=True)
    for directory in ("unit", "integration", "regression", "validation"):
        (root / "tests" / directory).mkdir(parents=True)
    (root / "src/example").mkdir(parents=True)
    (root / "sdlc_docs/01_requirements/product_requirements.md").write_text("# Approved requirements\n", encoding="utf-8")
    (root / "sdlc_docs/02_architecture/architecture.md").write_text("# Approved architecture\n", encoding="utf-8")
    (root / "sdlc_docs/03_implementation/backlog_priority.md").write_text(
        "# Backlog Priority Guidance\n\n| Issue | Status |\n|---|---|\n| US-0001 | Ready |\n",
        encoding="utf-8",
    )
    (root / "sdlc_docs/trace_workflow.md").write_text(
        "# Workflow Traceability\n\n"
        "| Item | Type | Status |\n"
        "|---|---|---|\n"
        "| Architecture | Initial Release | Complete |\n"
        "| Repository preparation | Initial Release | Complete |\n"
        f"| Technical foundation | Initial Release | {foundation_status} |\n"
        "| Implementation | Initial Release | In Progress |\n",
        encoding="utf-8",
    )
    (root / "pyproject.toml").write_text(
        "[project]\nname='example'\nversion='0.1.0'\ndependencies=[]\n"
        "[dependency-groups]\ndev=['pytest>=8','pytest-bdd>=8']\n",
        encoding="utf-8",
    )


def main() -> int:
    skill_text = SKILL_MD.read_text(encoding="utf-8")
    flow_text = FLOWCHART.read_text(encoding="utf-8")

    checks: list[tuple[str, bool]] = []
    checks.append(("frontmatter identifier", "name: g-implement-repository-work" in skill_text))
    checks.append(("operating modes", "Operating Modes" in skill_text and "Backlog priority planning mode" in skill_text and "Single issue implementation mode" in skill_text))
    checks.append(("one issue rule", "exactly one selected issue" in skill_text))
    checks.append(("03 implementation planning", "sdlc_docs/03_implementation/backlog_priority.md" in skill_text and "manual guidance" in skill_text))
    checks.append(("approval before writes", "before modifying repository files" in skill_text))
    checks.append(("tdd cycle", "RED -> GREEN -> REFACTOR" in skill_text))
    checks.append(("developer code design", "Developer Code Design" in skill_text and "sdlc_docs/02_architecture/code-level.md" in skill_text))
    checks.append(("hybrid code-level docs", "sdlc_docs/02_architecture/containers/<container>/code-level.md" in skill_text))
    checks.append(("mermaid code-level diagrams", "Mermaid diagrams" in skill_text and "sequence" in skill_text and "class" in skill_text))
    checks.append(("structurizr c4 boundary", "Structurizr DSL canonical for C4" in skill_text))
    checks.append(("best practices section", "Best Practices" in skill_text and "references/best-practices/README.md" in skill_text))
    checks.append(("ping pong tdd", "Ping-Pong TDD" in skill_text and "Tester driver" in skill_text and "Developer navigator" in skill_text))
    checks.append(("user visible tdd status", "which tests are proposed" in skill_text and "which tests are created" in skill_text and "current RED, GREEN, or REFACTOR status" in skill_text))
    checks.append(("tester defines before developer implements", "Tester driver` defines the intended behavior as failing tests" in skill_text and "Developer navigator` implements only enough production code" in skill_text))
    checks.append(("local status tracking rule", "sdlc_docs/trace_workflow.md" in skill_text and "sdlc_docs/03_implementation/backlog_priority.md" in skill_text and "local status-tracking" in skill_text))
    checks.append(("pytest policy", "Use `pytest` for new Python tests" in skill_text))
    checks.append(("bdd boundary", "Do not create product BDD scenarios" in skill_text))
    checks.append(("remote action boundary", "Do not commit, push, create pull requests" in skill_text))
    checks.append(("no persistent reports", "Do not create persistent TDD reports" in skill_text))

    implementation_workflow = re.search(r"## Single Issue Implementation Workflow(.*?)(?:\n## |\Z)", skill_text, re.S)
    priority_workflow = re.search(r"## Backlog Priority Planning Workflow(.*?)(?:\n## |\Z)", skill_text, re.S)
    checks.append(("priority workflow exists", priority_workflow is not None and [int(value) for value in re.findall(r"(?m)^(\d+)\. ", priority_workflow.group(1))] == list(range(1, 14))))
    checks.append(("implementation workflow exists", implementation_workflow is not None and [int(value) for value in re.findall(r"(?m)^(\d+)\. ", implementation_workflow.group(1))] == list(range(1, 32))))
    checks.append(("flowchart branches by mode", "Backlog priority planning" in flow_text and "Single issue implementation" in flow_text))
    checks.append(("flowchart mentions 03 implementation", "sdlc_docs/03_implementation" in flow_text))
    checks.append(("flowchart mentions mermaid purpose", "Mermaid diagrams document code-level" in flow_text))
    checks.append(("flowchart mentions tdd role names", "Tester driver" in flow_text and "Developer navigator" in flow_text))
    checks.append(("flowchart shows tester before developer", "Tester driver defines intended logic with tests before Developer navigator implements production code" in flow_text))
    checks.append(("flowchart mentions status tracking update", "Update local status-tracking docs" in flow_text and "remote issue/project state require separate approval" in flow_text))

    alias = "Run " + chr(ord("f") + 1)
    checks.append(("no single-letter invocation alias", alias not in skill_text and alias not in flow_text))

    golden_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(GOLDEN.glob("*.md")))
    checks.append(("golden continues browser task board", "US-0001 - Create a task" in golden_text))
    checks.append(("golden shows red green refactor", all(token in golden_text for token in ("RED", "GREEN", "REFACTOR"))))
    checks.append(("golden shows code design", "code-level design" in golden_text.casefold() and "code-level.md" in golden_text))
    checks.append(("golden shows backlog priority", "backlog_priority.md" in golden_text and "Manual priority guidance" in golden_text))
    checks.append(("golden shows mermaid", "```mermaid" in golden_text and "sequenceDiagram" in golden_text))
    checks.append(("golden shows best practices", "Best-practice references" in golden_text))
    checks.append(("golden shows ping pong roles", "Tester driver" in golden_text and "Developer navigator" in golden_text))
    checks.append(("golden shows user visible tdd status", "User-visible status" in golden_text and "Created test" in golden_text and "Current status" in golden_text))
    checks.append(("golden shows developer waits for red", "Developer navigator status: waiting" in golden_text and "Developer navigator response" in golden_text))
    checks.append(("golden shows local status tracking", "workflow traceability" in golden_text.casefold() and "Implementation status" in golden_text and "backlog_priority.md" in golden_text))
    checks.append(("golden performs no remote action", "None performed" in golden_text))

    best_practices_index = SKILL_ROOT / "references/best-practices/README.md"
    python_best_practices = SKILL_ROOT / "references/best-practices/python-best-practices.md"
    checks.append(("best-practices index exists", best_practices_index.is_file()))
    checks.append(("python best-practices reference exists", python_best_practices.is_file()))
    checks.append(("best-practices index links python reference", "python-best-practices.md" in best_practices_index.read_text(encoding="utf-8")))
    checks.append(("skill points to python best practices", "references/best-practices/python-best-practices.md" in skill_text))
    checks.append(("code design policy exists", (SKILL_ROOT / "references/code-design-policy.md").is_file()))
    backlog_policy = SKILL_ROOT / "references/backlog-priority-policy.md"
    checks.append(("backlog priority policy exists", backlog_policy.is_file()))
    checks.append(("skill links backlog priority policy", "references/backlog-priority-policy.md" in skill_text))
    checks.append(("code design policy explains hybrid docs", "Hybrid Code-Level Architecture" in (SKILL_ROOT / "references/code-design-policy.md").read_text(encoding="utf-8")))

    for asset in sorted((SKILL_ROOT / "assets").glob("*.py")):
        compile(asset.read_text(encoding="utf-8"), str(asset), "exec")
    checks.append(("python assets compile", True))

    with tempfile.TemporaryDirectory() as temporary:
        repo = Path(temporary)
        create_repo(repo)
        inspected = run([sys.executable, str(INSPECTOR), str(repo), "--mode", "single-issue", "--issue", "US-0001"], expected=0)
        inspected_payload = json.loads(inspected.stdout)
        checks.append(("ready repository inspection", inspected_payload["ready"] is True))
        checks.append(("readiness reports mode", inspected_payload["mode"] == "single-issue"))
        checks.append(("readiness reports implementation docs", inspected_payload["implementation_documents"]["directory"] is True))
        checks.append(("readiness reports implementation workflow status", inspected_payload["workflow_status"]["Implementation"] == "In Progress"))
        checks.append(("readiness reports central code-level document", inspected_payload["code_level_documents"]["central_index"] is False))
        checks.append(("readiness reports per-container code-level documents", inspected_payload["code_level_documents"]["per_container"]["sdlc_docs/02_architecture/containers/flask-backend"] is False))
        checks.append(("readiness reports best-practice references", "references/best-practices/README.md" in inspected_payload["best_practice_references"]))
        checks.append(("readiness reports python best practices", "references/best-practices/python-best-practices.md" in inspected_payload["best_practice_references"]))
        planning = run([sys.executable, str(INSPECTOR), str(repo), "--mode", "backlog-priority"], expected=0)
        checks.append(("backlog priority inspection does not require issue", json.loads(planning.stdout)["ready"] is True))

        not_ready = repo / "not-ready"
        create_repo(not_ready, foundation_status="Pending Approval")
        run([sys.executable, str(INSPECTOR), str(not_ready), "--mode", "single-issue", "--issue", "US-0001"], expected=1)
        checks.append(("incomplete foundation blocks readiness", True))

        test_file = repo / "tests/unit/test_example.py"
        test_file.write_text("import pytest\n\npytestmark = pytest.mark.unit\n\ndef test_example():\n    assert True\n", encoding="utf-8")
        source_file = repo / "src/example/service.py"
        source_file.write_text("VALUE = 1\n", encoding="utf-8")
        code_level = repo / "sdlc_docs/02_architecture/code-level.md"
        code_level.write_text("# Code-Level Implementation Map\n\n```mermaid\nsequenceDiagram\n    A->>B: call\n```\n", encoding="utf-8")
        valid = run([
            sys.executable,
            str(VALIDATOR),
            str(repo),
            "--issue",
            "US-0001",
            "--changed-file",
            "sdlc_docs/trace_workflow.md",
            "--changed-file",
            "sdlc_docs/03_implementation/backlog_priority.md",
            "--changed-file",
            "sdlc_docs/02_architecture/code-level.md",
            "--changed-file",
            "src/example/service.py",
            "--changed-file",
            "tests/unit/test_example.py",
        ], expected=0)
        valid_payload = json.loads(valid.stdout)
        checks.append(("story with production and pytest changes validates", valid_payload["valid"] is True))
        checks.append(("validator reports local status tracking", valid_payload["local_status_tracking"]["trace_workflow"]["changed"] is True and valid_payload["local_status_tracking"]["backlog_priority"]["changed"] is True))

        no_trace = run([
            sys.executable,
            str(VALIDATOR),
            str(repo),
            "--issue",
            "US-0001",
            "--changed-file",
            "sdlc_docs/02_architecture/code-level.md",
            "--changed-file",
            "src/example/service.py",
            "--changed-file",
            "tests/unit/test_example.py",
        ], expected=0)
        no_trace_warnings = json.loads(no_trace.stdout)["warnings"]
        checks.append(("production change without trace update warns", any("trace_workflow.md" in warning for warning in no_trace_warnings)))
        checks.append(("production change without backlog status update warns", any("backlog_priority.md" in warning for warning in no_trace_warnings)))

        run([
            sys.executable,
            str(VALIDATOR),
            str(repo),
            "--issue",
            "US-0001",
            "--changed-file",
            "sdlc_docs/trace_workflow.md",
            "--changed-file",
            "sdlc_docs/03_implementation/backlog_priority.md",
            "--changed-file",
            "sdlc_docs/02_architecture/code-level.md",
            "--changed-file",
            "src/example/service.py",
        ], expected=1)
        checks.append(("production change without tests is rejected", True))

        code_level.unlink()
        run([
            sys.executable,
            str(VALIDATOR),
            str(repo),
            "--issue",
            "US-0001",
            "--changed-file",
            "src/example/service.py",
            "--changed-file",
            "tests/unit/test_example.py",
        ], expected=1)
        checks.append(("production change without code-level map is rejected", True))
        per_container_code_level = repo / "sdlc_docs/02_architecture/containers/flask-backend/code-level.md"
        per_container_code_level.write_text("# Flask Backend Code-Level Map\n\n```mermaid\nclassDiagram\n    TaskService --> RepositoryPort\n```\n", encoding="utf-8")
        per_container_valid = run([
            sys.executable,
            str(VALIDATOR),
            str(repo),
            "--issue",
            "US-0001",
            "--changed-file",
            "sdlc_docs/02_architecture/containers/flask-backend/code-level.md",
            "--changed-file",
            "src/example/service.py",
            "--changed-file",
            "tests/unit/test_example.py",
        ], expected=0)
        checks.append(("per-container code-level map validates", json.loads(per_container_valid.stdout)["valid"] is True))
        code_level.write_text("# Code-Level Implementation Map\n\n```mermaid\nsequenceDiagram\n    A->>B: call\n```\n", encoding="utf-8")

        regression_file = repo / "tests/regression/test_issue_42.py"
        regression_file.write_text("import pytest\n\npytestmark=[pytest.mark.regression, pytest.mark.unit]\n\ndef test_issue_42():\n    assert True\n", encoding="utf-8")
        run([
            sys.executable,
            str(VALIDATOR),
            str(repo),
            "--issue",
            "BUG-42",
            "--work-type",
            "bug",
            "--changed-file",
            "sdlc_docs/trace_workflow.md",
            "--changed-file",
            "sdlc_docs/03_implementation/backlog_priority.md",
            "--changed-file",
            "sdlc_docs/02_architecture/code-level.md",
            "--changed-file",
            "src/example/service.py",
            "--changed-file",
            "tests/regression/test_issue_42.py",
        ], expected=0)
        checks.append(("bug with regression test validates", True))

    for name, condition in checks:
        check(condition, name)
        print(f"PASS: {name}")
    print(f"PASS: {len(checks)} regression checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
