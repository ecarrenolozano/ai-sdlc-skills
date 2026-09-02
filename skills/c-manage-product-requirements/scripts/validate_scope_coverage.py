#!/usr/bin/env python3
"""Validate source statements, atomic capabilities, story mappings, and report synchronization."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

EXIT_VALIDATION_FAILED = 1
EXIT_EXECUTION_ERROR = 2

SOURCE_REGISTER_COLUMNS = [
    "Source ID",
    "Source scope statement",
    "Source location",
    "Statement role",
    "Decomposed into CAP IDs",
    "Rationale",
]

COVERAGE_COLUMNS = [
    "Scope ID",
    "Atomic capability",
    "Source IDs",
    "Source scope statement",
    "Source location",
    "Disposition",
    "Requirement / Stories",
    "Rationale or approval evidence",
]

ALLOWED_SOURCE_ROLES = {"atomic", "compound", "umbrella"}
ALLOWED_DISPOSITIONS = {
    "covered",
    "grouped",
    "pending clarification",
    "deferred by approved decision",
    "excluded by approved decision",
}

ACTION_VERBS = {
    "add", "approve", "assign", "cancel", "change", "close", "collaborate",
    "configure", "create", "delete", "deselect", "disable", "display",
    "download", "edit", "enable", "export", "filter", "import", "invite",
    "load", "move", "open", "preserve", "receive", "reject", "remove",
    "restore", "retry", "save", "schedule", "search", "select", "send",
    "share", "sort", "submit", "unassign", "update", "upload", "view",
}

UMBRELLA_VERBS = {
    "administer", "handle", "maintain", "manage", "operate", "support",
}


def normalize(text: str) -> str:
    text = text.replace("`", "").replace("—", "-")
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text.rstrip(".;:")


def heading_level(line: str) -> int | None:
    match = re.match(r"^(#{1,6})\s+", line)
    return len(match.group(1)) if match else None


def collect_bullets_under_heading(lines: list[str], start: int, level: int) -> list[str]:
    bullets: list[str] = []
    index = start + 1
    while index < len(lines):
        current_level = heading_level(lines[index])
        if current_level is not None and current_level <= level:
            break
        match = re.match(r"^\s*-\s+(.*\S)\s*$", lines[index])
        if match:
            bullets.append(match.group(1).strip())
        elif bullets and lines[index].strip().endswith(":"):
            break
        index += 1
    return bullets


def extract_initial_release_source_statements(text: str) -> list[str]:
    lines = text.splitlines()
    included: list[str] = []
    success: list[str] = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^###\s+Included High-Level Capabilities\s*$", stripped, re.I):
            included.extend(collect_bullets_under_heading(lines, index, 3))
        elif re.match(r"^##\s+(?:\d+\.\s*)?Success Criteria\s*$", stripped, re.I):
            success.extend(collect_bullets_under_heading(lines, index, 2))

    statements = included if included else success
    unique: list[str] = []
    seen: set[str] = set()
    for statement in statements:
        key = normalize(statement)
        if key and key not in seen:
            unique.append(statement)
            seen.add(key)
    return unique


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_table_after_heading(
    text: str,
    heading_pattern: str,
    required_columns: list[str],
    label: str,
) -> tuple[list[dict[str, str]], list[str]]:
    lines = text.splitlines()
    errors: list[str] = []
    heading_index = next(
        (i for i, line in enumerate(lines) if re.match(heading_pattern, line.strip(), re.I)),
        None,
    )
    if heading_index is None:
        return [], [f"Missing '{label}' heading."]

    table_start = None
    for index in range(heading_index + 1, min(len(lines), heading_index + 16)):
        if lines[index].lstrip().startswith("|"):
            table_start = index
            break
    if table_start is None or table_start + 1 >= len(lines):
        return [], [f"{label} table is missing or incomplete."]

    headers = split_markdown_row(lines[table_start])
    missing = [column for column in required_columns if column not in headers]
    if missing:
        return [], [f"{label} missing columns: {', '.join(missing)}"]

    separator = split_markdown_row(lines[table_start + 1])
    if len(separator) != len(headers) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        return [], [f"{label} separator row is invalid."]

    rows: list[dict[str, str]] = []
    for line in lines[table_start + 2 :]:
        if not line.lstrip().startswith("|"):
            break
        cells = split_markdown_row(line)
        if len(cells) != len(headers):
            errors.append(f"{label} row has {len(cells)} cells; expected {len(headers)}: {line.strip()}")
            continue
        row = dict(zip(headers, cells, strict=True))
        if any(value.strip() for value in row.values()):
            rows.append(row)
    if not rows:
        errors.append(f"{label} has no data rows.")
    return rows, errors


def parse_source_register(text: str) -> tuple[list[dict[str, str]], list[str]]:
    return parse_table_after_heading(
        text,
        r"^###\s+Source Statement Coverage Register\s*$",
        SOURCE_REGISTER_COLUMNS,
        "Source Statement Coverage Register",
    )


def parse_coverage_matrix(text: str) -> tuple[list[dict[str, str]], list[str]]:
    return parse_table_after_heading(
        text,
        r"^###\s+Source Scope Coverage Matrix\s*$",
        COVERAGE_COLUMNS,
        "Source Scope Coverage Matrix",
    )


def parse_ids(text: str, prefix: str) -> list[str]:
    return re.findall(rf"{re.escape(prefix)}-\d+", text)


def parse_story_blocks(text: str) -> dict[str, dict[str, object]]:
    lines = text.splitlines()
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^###\s+(US-\d+)\s+[—-]\s+(.+?)\s*$", line.strip())
        if match:
            starts.append((index, match.group(1), match.group(2)))

    stories: dict[str, dict[str, object]] = {}
    for position, (start, story_id, title) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        for index in range(start + 1, end):
            if re.match(r"^##\s+REQ-", lines[index].strip()) or re.match(
                r"^###\s+Requirement Validation", lines[index].strip(), re.I
            ):
                end = index
                break
        block = lines[start:end]
        metadata: dict[str, str] = {}
        for line in block:
            match = re.match(r"^-\s+\*\*(Covered scope IDs|Atomicity):\*\*\s*(.*)$", line.strip(), re.I)
            if match:
                metadata[match.group(1).lower()] = match.group(2).strip()
        want_line = next((line.strip() for line in block if re.match(r"^I want\b", line.strip(), re.I)), "")
        stories[story_id] = {
            "title": title,
            "covered_scope_ids": parse_ids(metadata.get("covered scope ids", ""), "CAP"),
            "atomicity": metadata.get("atomicity", ""),
            "want_line": want_line,
        }
    return stories


def parse_requirement_reports(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^##\s+(REQ-\d+)\s+[—-]", line.strip())
        if match:
            starts.append((index, match.group(1)))

    reports: list[dict[str, str]] = []
    for position, (start, req_id) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        values: dict[str, str] = {"requirement": req_id}
        for line in block:
            match = re.match(
                r"^-\s+\*\*(Status|Scope coverage validator|Scope validator command|Scope validator report synchronized):\*\*\s*(.*)$",
                line.strip(),
                re.I,
            )
            if match:
                values[normalize(match.group(1))] = match.group(2).strip()
        if any(key in values for key in ("scope coverage validator", "scope validator command")):
            reports.append(values)
    return reports


def contains_compound_actions(text: str) -> bool:
    normalized = normalize(text)
    if " and " not in normalized and " or " not in normalized:
        return False
    tokens = re.findall(r"[a-z]+", normalized)
    verbs = [token for token in tokens if token in ACTION_VERBS or token in UMBRELLA_VERBS]
    return len(set(verbs)) >= 2


def contains_umbrella_action(text: str) -> bool:
    tokens = set(re.findall(r"[a-z]+", normalize(text)))
    return bool(tokens & UMBRELLA_VERBS)


def approved_grouping(text: str) -> bool:
    lowered = normalize(text)
    return lowered.startswith("approved grouping -") and len(lowered.split()) >= 4


def expected_report_status(requirement_status: str, has_errors: bool) -> str:
    if has_errors:
        return "Failed"
    status = normalize(requirement_status)
    if status in {"approved", "pending approval"}:
        return "Passed"
    return "Preflight passed"


def validate(source_text: str, requirements_text: str, mode: str, require_report_sync: bool) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    source_rows, source_errors = parse_source_register(requirements_text)
    coverage_rows, coverage_errors = parse_coverage_matrix(requirements_text)
    errors.extend(source_errors)
    errors.extend(coverage_errors)
    stories = parse_story_blocks(requirements_text)

    by_source_id: dict[str, dict[str, str]] = {}
    source_statement_to_row: dict[str, dict[str, str]] = {}
    source_to_caps: dict[str, set[str]] = defaultdict(set)

    for row in source_rows:
        source_id = row["Source ID"].strip()
        if not re.fullmatch(r"SRC-\d{3,}", source_id):
            errors.append(f"Invalid Source ID '{source_id}'. Expected SRC-NNN.")
        elif source_id in by_source_id:
            errors.append(f"Duplicate Source ID '{source_id}'.")
        else:
            by_source_id[source_id] = row

        statement = row["Source scope statement"].strip()
        statement_key = normalize(statement)
        if not statement:
            errors.append(f"{source_id or '<missing ID>'}: source scope statement is empty.")
        elif statement_key in source_statement_to_row:
            errors.append(f"Duplicate source statement in register: {statement}")
        else:
            source_statement_to_row[statement_key] = row

        role = normalize(row["Statement role"])
        if role not in ALLOWED_SOURCE_ROLES:
            errors.append(f"{source_id or '<missing ID>'}: unsupported statement role '{row['Statement role']}'.")

        cap_ids = parse_ids(row["Decomposed into CAP IDs"], "CAP")
        for cap_id in cap_ids:
            source_to_caps[source_id].add(cap_id)

        if role == "atomic" and len(cap_ids) != 1:
            errors.append(f"{source_id}: Atomic source statement must map to exactly one CAP ID.")
        if role == "compound" and len(set(cap_ids)) < 2:
            errors.append(f"{source_id}: Compound source statement must map to at least two CAP IDs.")
        if role == "umbrella":
            if len(set(cap_ids)) < 2:
                errors.append(f"{source_id}: Umbrella source statement must decompose into at least two CAP IDs.")
            if not normalize(row["Rationale"]).startswith("umbrella decomposition -"):
                errors.append(f"{source_id}: Umbrella role requires 'Umbrella decomposition — <rationale>'.")

        if contains_umbrella_action(statement) and role != "umbrella":
            errors.append(f"{source_id}: source statement uses an umbrella action and must have role Umbrella: {statement}")
        if role == "atomic" and contains_compound_actions(statement):
            errors.append(f"{source_id}: compound source statement cannot have role Atomic: {statement}")

    by_scope_id: dict[str, dict[str, str]] = {}
    story_to_matrix_scope_ids: dict[str, set[str]] = defaultdict(set)
    cap_to_sources: dict[str, set[str]] = defaultdict(set)

    for row in coverage_rows:
        scope_id = row["Scope ID"].strip()
        if not re.fullmatch(r"CAP-\d{3,}", scope_id):
            errors.append(f"Invalid Scope ID '{scope_id}'. Expected CAP-NNN.")
        elif scope_id in by_scope_id:
            errors.append(f"Duplicate Scope ID '{scope_id}'.")
        else:
            by_scope_id[scope_id] = row

        capability = row["Atomic capability"].strip()
        if not capability:
            errors.append(f"{scope_id or '<missing ID>'}: atomic capability is empty.")
        if contains_umbrella_action(capability):
            errors.append(f"{scope_id or '<missing ID>'}: umbrella action is not an atomic capability: {capability}")
        if contains_compound_actions(capability):
            errors.append(f"{scope_id or '<missing ID>'}: atomic capability contains multiple actions: {capability}")

        source_ids = parse_ids(row["Source IDs"], "SRC")
        if not source_ids:
            errors.append(f"{scope_id or '<missing ID>'}: missing Source IDs.")
        for source_id in source_ids:
            cap_to_sources[scope_id].add(source_id)
            if source_id not in by_source_id:
                errors.append(f"{scope_id or '<missing ID>'}: references unknown source ID '{source_id}'.")
            elif scope_id not in source_to_caps.get(source_id, set()):
                errors.append(f"{scope_id}: source ID '{source_id}' does not map back to this CAP in the source register.")

        disposition = normalize(row["Disposition"])
        if disposition not in ALLOWED_DISPOSITIONS:
            errors.append(f"{scope_id or '<missing ID>'}: unsupported disposition '{row['Disposition']}'.")

        story_ids = parse_ids(row["Requirement / Stories"], "US")
        rationale = row["Rationale or approval evidence"].strip()
        if disposition in {"covered", "grouped"} and not story_ids:
            errors.append(f"{scope_id}: {row['Disposition']} requires at least one story reference.")
        if disposition == "grouped" and not approved_grouping(rationale):
            errors.append(f"{scope_id}: Grouped requires explicit 'Approved grouping — <rationale>' evidence.")
        if disposition in {"deferred by approved decision", "excluded by approved decision"}:
            if "approved" not in normalize(rationale) or len(rationale.split()) < 4:
                errors.append(f"{scope_id}: deferred/excluded disposition requires approved-decision evidence.")

        for story_id in story_ids:
            story_to_matrix_scope_ids[story_id].add(scope_id)
            if story_id not in stories:
                errors.append(f"{scope_id}: references missing story '{story_id}'.")

    for source_id, cap_ids in source_to_caps.items():
        for cap_id in cap_ids:
            if cap_id not in by_scope_id:
                errors.append(f"{source_id}: references missing capability '{cap_id}'.")
            elif source_id not in cap_to_sources.get(cap_id, set()):
                errors.append(f"{source_id}: CAP '{cap_id}' does not map back to this source in the coverage matrix.")

    canonical_source_statements: list[str] = []
    if mode == "initial-release":
        canonical_source_statements = extract_initial_release_source_statements(source_text)
        if not canonical_source_statements:
            errors.append("No source statements found under Included High-Level Capabilities or Success Criteria.")
        for statement in canonical_source_statements:
            if normalize(statement) not in source_statement_to_row:
                errors.append(f"Source scope statement omitted from source register: {statement}")
        canonical_keys = {normalize(statement) for statement in canonical_source_statements}
        for statement_key, row in source_statement_to_row.items():
            if statement_key not in canonical_keys:
                errors.append(f"Source register contains a statement not found in the canonical source scope: {row['Source scope statement']}")

    for story_id, story in stories.items():
        covered_ids = list(story["covered_scope_ids"])
        atomicity = str(story["atomicity"])
        if not covered_ids:
            errors.append(f"{story_id}: missing Covered scope IDs metadata.")
        for scope_id in covered_ids:
            if scope_id not in by_scope_id:
                errors.append(f"{story_id}: references unknown scope ID '{scope_id}'.")
            elif story_id not in parse_ids(by_scope_id[scope_id]["Requirement / Stories"], "US"):
                errors.append(f"{story_id}: scope ID '{scope_id}' does not map back to the story in the coverage matrix.")

        matrix_ids = story_to_matrix_scope_ids.get(story_id, set())
        if set(covered_ids) != matrix_ids:
            errors.append(f"{story_id}: Covered scope IDs {sorted(covered_ids)} do not match matrix mappings {sorted(matrix_ids)}.")

        if not atomicity:
            errors.append(f"{story_id}: missing Atomicity metadata.")
        grouped = approved_grouping(atomicity)
        if len(covered_ids) > 1 and not grouped:
            errors.append(f"{story_id}: multiple capabilities require 'Approved grouping — <rationale>'.")
        if contains_umbrella_action(str(story["title"])) or contains_umbrella_action(str(story["want_line"])):
            if not grouped:
                errors.append(f"{story_id}: umbrella action is not a single observable story outcome.")
        if contains_compound_actions(str(story["title"])) or contains_compound_actions(str(story["want_line"])):
            if not grouped:
                errors.append(f"{story_id}: story combines independent user actions without approved grouping.")

    active_state_match = re.search(r"^-\s+\*\*Active scope state:\*\*\s*(.+)$", requirements_text, re.M | re.I)
    active_state = normalize(active_state_match.group(1)) if active_state_match else ""
    if active_state in {"pending approval", "approved"}:
        for row in coverage_rows:
            if normalize(row["Disposition"]) == "pending clarification":
                errors.append(f"{row['Scope ID']}: Pending clarification is not allowed when the active scope is {active_state}.")

    structural_errors = list(errors)
    reports = parse_requirement_reports(requirements_text)
    report_results: list[dict[str, object]] = []
    if require_report_sync:
        if not reports:
            errors.append("No Requirement Validation report contains scope-validator synchronization fields.")
        for report in reports:
            expected = expected_report_status(report.get("status", ""), bool(structural_errors))
            actual = report.get("scope coverage validator", "")
            command = report.get("scope validator command", "")
            synchronized = normalize(report.get("scope validator report synchronized", ""))
            ok = normalize(actual) == normalize(expected)
            if not ok:
                errors.append(
                    f"{report['requirement']}: Scope coverage validator report is '{actual or '<missing>'}', expected '{expected}'."
                )
            if ".agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py" not in command:
                errors.append(f"{report['requirement']}: Scope validator command is missing or does not use the required path.")
                ok = False
            if synchronized != "yes":
                errors.append(f"{report['requirement']}: Scope validator report synchronized must be Yes.")
                ok = False
            report_results.append({
                "requirement": report["requirement"],
                "expected": expected,
                "actual": actual,
                "synchronized": ok,
            })
    else:
        for report in reports:
            report_results.append({
                "requirement": report["requirement"],
                "expected": expected_report_status(report.get("status", ""), bool(structural_errors)),
                "actual": report.get("scope coverage validator", ""),
                "synchronized": None,
            })

    return {
        "passed": not errors,
        "mode": mode,
        "source_scope_statements": canonical_source_statements,
        "source_register_rows": len(source_rows),
        "coverage_rows": len(coverage_rows),
        "stories": sorted(stories),
        "require_report_sync": require_report_sync,
        "requirement_reports": report_results,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Approved Project Context or imported source issue")
    parser.add_argument("requirements", type=Path, help="Product Requirements markdown file")
    parser.add_argument("--mode", choices=["initial-release", "product-increment"], required=True)
    parser.add_argument(
        "--require-report-sync",
        action="store_true",
        help="Require every active Requirement Validation block to match the validator result and command.",
    )
    args = parser.parse_args()

    try:
        source_text = args.source.read_text(encoding="utf-8")
        requirements_text = args.requirements.read_text(encoding="utf-8")
        result = validate(source_text, requirements_text, args.mode, args.require_report_sync)
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"passed": False, "execution_error": str(exc)}, indent=2))
        return EXIT_EXECUTION_ERROR

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else EXIT_VALIDATION_FAILED


if __name__ == "__main__":
    sys.exit(main())
