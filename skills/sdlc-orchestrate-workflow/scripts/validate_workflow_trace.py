#!/usr/bin/env python3
"""Validate SDLC workflow trace shape, statuses, and next-action identifiers."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {
    "Not Started",
    "In Progress",
    "Under Clarification",
    "Pending Approval",
    "Complete",
    "Blocked",
}

KNOWN_SKILLS = {
    "sdlc-bootstrap-project",
    "a-clarify-project-request",
    "b-form-project-context",
    "c-manage-product-requirements",
    "d-design-product-architecture",
    "e-sync-repository-requirements",
    "f-establish-technical-foundation",
    "g-implement-repository-work",
    "i-validate-user-story-completion",
    "h-create-implementation-pull-request",
    "j-prepare-release-deployment",
    "sdlc-orchestrate-workflow",
}


ROW_ORDER = [
    "Project request", "Project context", "Initial requirements", "Architecture",
    "Repository preparation", "Technical foundation", "Implementation",
    "User story validation", "Pull request", "Release deployment",
]
INCOMPLETE = {"Not Started", "In Progress", "Under Clarification", "Pending Approval", "Blocked"}

EXPECTED_ROWS = {
    "Project request",
    "Project context",
    "Initial requirements",
    "Architecture",
    "Repository preparation",
    "Technical foundation",
    "Implementation",
    "User story validation",
    "Pull request",
    "Release deployment",
}

HEADER = ["Item", "Type", "Status", "Current activity", "Evidence", "Missing or blocked", "Next action"]
HYPHEN_TOKEN_RE = re.compile(r"\b([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\b")
SINGLE_LETTER_ALIAS_RE = re.compile(r"\b(?:Run|Continue)\s+([A-J])\b")


def split_row(line: str) -> list[str]:
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def parse_trace(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    rows: list[dict[str, str]] = []
    if not path.is_file():
        return rows, [f"missing trace file: {path}"]
    lines = path.read_text(encoding="utf-8").splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return rows, ["trace file does not contain a markdown table"]
    header = split_row(table_lines[0])
    if header != HEADER:
        errors.append(f"unexpected trace header: {header}")
        return rows, errors
    for line in table_lines[2:]:
        cells = split_row(line)
        if len(cells) != len(HEADER):
            errors.append(f"row has {len(cells)} cells instead of {len(HEADER)}: {line}")
            continue
        rows.append(dict(zip(HEADER, cells, strict=True)))
    return rows, errors


def validate(path: Path, require_expected_rows: bool) -> dict[str, Any]:
    rows, errors = parse_trace(path)
    warnings: list[str] = []

    row_names = {row["Item"] for row in rows}
    if require_expected_rows:
        for missing in sorted(EXPECTED_ROWS - row_names):
            errors.append(f"missing expected row: {missing}")

    active_rows = []
    for row in rows:
        item = row["Item"]
        status = row["Status"]
        evidence = row["Evidence"]
        blocker = row["Missing or blocked"]
        next_action = row["Next action"]

        if status not in ALLOWED_STATUSES:
            errors.append(f"{item}: unsupported status {status!r}")
        if status in {"In Progress", "Under Clarification", "Pending Approval", "Blocked"}:
            active_rows.append(item)
        if status == "Complete" and evidence in {"", "None", "TBD", "Not created"}:
            warnings.append(f"{item}: complete row has weak evidence")
        if status == "Blocked" and blocker in {"", "None", "TBD"}:
            errors.append(f"{item}: blocked row must name a blocker")
        if status == "Pending Approval" and "approval" not in next_action.casefold() and "review" not in next_action.casefold():
            warnings.append(f"{item}: pending approval row should point to review or approval")

        for alias in SINGLE_LETTER_ALIAS_RE.findall(next_action):
            errors.append(f"{item}: single-letter skill alias in Next action: {alias}")

        for match in HYPHEN_TOKEN_RE.findall(next_action):
            looks_like_skill = match in KNOWN_SKILLS or re.match(r"^[a-j]-", match) or match.startswith("sdlc-")
            if looks_like_skill and match not in KNOWN_SKILLS:
                errors.append(f"{item}: unknown skill identifier in Next action: {match}")

    row_by_name = {row["Item"]: row for row in rows}
    implementation_status = row_by_name.get("Implementation", {}).get("Status")
    validation_status = row_by_name.get("User story validation", {}).get("Status")
    pull_request_status = row_by_name.get("Pull request", {}).get("Status")
    release_status = row_by_name.get("Release deployment", {}).get("Status")
    allowed_validation_overlap = (
        set(active_rows) == {"Implementation", "User story validation"}
        and implementation_status == "In Progress"
        and validation_status == "In Progress"
    )
    allowed_pull_request_overlap = (
        set(active_rows) == {"Implementation", "Pull request"}
        and implementation_status == "In Progress"
        and pull_request_status == "In Progress"
    )
    allowed_release_overlap = (
        set(active_rows) == {"Implementation", "Release deployment"}
        and implementation_status == "In Progress"
        and release_status == "In Progress"
    )
    allowed_pull_release_overlap = (
        set(active_rows) == {"Implementation", "Pull request", "Release deployment"}
        and implementation_status == "In Progress"
        and pull_request_status == "In Progress"
        and release_status == "In Progress"
    )
    allowed_overlap = (
        allowed_validation_overlap
        or allowed_pull_request_overlap
        or allowed_release_overlap
        or allowed_pull_release_overlap
    )

    if len(active_rows) > 1 and not allowed_overlap:
        warnings.append(f"multiple active rows: {', '.join(active_rows)}")

    for index, item in enumerate(ROW_ORDER):
        row = row_by_name.get(item)
        if not row or row["Status"] == "Not Started":
            continue
        incomplete_upstream = [name for name in ROW_ORDER[:index] if name in row_by_name and row_by_name[name]["Status"] != "Complete"]
        if incomplete_upstream:
            if item == "User story validation":
                only_implementation_is_incomplete = set(incomplete_upstream) == {"Implementation"}
                if (
                    row["Status"] == "In Progress"
                    and only_implementation_is_incomplete
                    and implementation_status == "In Progress"
                ):
                    continue
            if item == "Pull request":
                allowed_incomplete_upstream = set(incomplete_upstream).issubset(
                    {"Implementation", "User story validation"}
                )
                if (
                    row["Status"] == "In Progress"
                    and allowed_incomplete_upstream
                    and implementation_status == "In Progress"
                ):
                    continue
            if item == "Release deployment":
                allowed_incomplete_upstream = set(incomplete_upstream).issubset(
                    {"Implementation", "User story validation", "Pull request"}
                )
                if (
                    row["Status"] == "In Progress"
                    and allowed_incomplete_upstream
                    and implementation_status == "In Progress"
                ):
                    continue
            errors.append(f"{item}: active before upstream gates are complete: {', '.join(incomplete_upstream)}")

    names_in_order = [row["Item"] for row in rows]
    if "Pull request" in row_names and "User story validation" not in row_names:
        warnings.append("pull request row exists without user story validation row")
    if "Release deployment" in row_names and "User story validation" not in row_names:
        warnings.append("release deployment row exists without user story validation row")
    if "User story validation" in row_names and "Pull request" in row_names:
        if names_in_order.index("User story validation") > names_in_order.index("Pull request"):
            errors.append("User story validation row must appear before Pull request row")
    if "Pull request" in row_names and "Release deployment" in row_names:
        if names_in_order.index("Pull request") > names_in_order.index("Release deployment"):
            errors.append("Pull request row must appear before Release deployment row")

    return {
        "passed": not errors,
        "trace_file": str(path),
        "row_count": len(rows),
        "active_rows": active_rows,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace_file", type=Path)
    parser.add_argument("--require-expected-rows", action="store_true")
    args = parser.parse_args()

    result = validate(args.trace_file, args.require_expected_rows)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
