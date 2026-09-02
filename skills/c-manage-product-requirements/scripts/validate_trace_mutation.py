#!/usr/bin/env python3
"""Validate that a Markdown traceability table changed only in authorized fields."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


@dataclass
class TraceTable:
    headers: list[str]
    rows: dict[str, dict[str, str]]
    order: list[str]
    outside: str


def parse_table(path: Path) -> TraceTable:
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if "|" not in line:
            continue
        cells = [norm(c) for c in line.strip().strip("|").split("|")]
        if "Item" not in cells:
            continue
        if i + 1 >= len(lines) or not re.fullmatch(r"\s*\|?[\s:|\-]+\|?\s*", lines[i + 1]):
            continue
        headers = cells
        rows: dict[str, dict[str, str]] = {}
        order: list[str] = []
        end = i + 2
        for end, row_line in enumerate(lines[i + 2 :], start=i + 2):
            if "|" not in row_line or not row_line.strip().startswith("|"):
                break
            values = [norm(c) for c in row_line.strip().strip("|").split("|")]
            if len(values) != len(headers):
                break
            row = dict(zip(headers, values, strict=True))
            item = row.get("Item", "")
            if not item:
                continue
            if item in rows:
                raise ValueError(f"Duplicate Item row {item!r} in {path}")
            rows[item] = row
            order.append(item)
        else:
            end = len(lines)
        prefix = "\n".join(lines[:i]).strip()
        suffix = "\n".join(lines[end:]).strip()
        outside = prefix + "\n<TRACE_TABLE>\n" + suffix
        return TraceTable(headers, rows, order, outside)
    raise ValueError(f"No Markdown table with an Item column found in {path}")


def parse_allow_field(raw: str) -> tuple[str, str]:
    if ":" not in raw:
        raise argparse.ArgumentTypeError("Expected ITEM:FIELD")
    item, field = raw.split(":", 1)
    return norm(item), norm(field)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--allow-field", action="append", default=[], type=parse_allow_field)
    parser.add_argument("--allow-add-row", action="append", default=[])
    parser.add_argument("--allow-remove-row", action="append", default=[])
    args = parser.parse_args()

    before = parse_table(args.before)
    after = parse_table(args.after)
    authorized_fields = set(args.allow_field)
    allow_add = {norm(x) for x in args.allow_add_row}
    allow_remove = {norm(x) for x in args.allow_remove_row}

    changes: list[dict[str, str]] = []
    unauthorized: list[dict[str, str]] = []

    def record(change: dict[str, str], allowed: bool) -> None:
        changes.append(change)
        if not allowed:
            unauthorized.append(change)

    if before.headers != after.headers:
        record({
            "item": "<table>",
            "field": "headers",
            "before": " | ".join(before.headers),
            "after": " | ".join(after.headers),
        }, False)

    if before.outside != after.outside:
        record({
            "item": "<document>",
            "field": "outside_table_content",
            "before": before.outside,
            "after": after.outside,
        }, False)

    common_before = [item for item in before.order if item in after.rows]
    common_after = [item for item in after.order if item in before.rows]
    if common_before != common_after:
        record({
            "item": "<table>",
            "field": "existing_row_order",
            "before": " -> ".join(common_before),
            "after": " -> ".join(common_after),
        }, False)

    all_items = list(dict.fromkeys(before.order + after.order))
    for item in all_items:
        if item not in before.rows:
            record({"item": item, "field": "__row_added__", "before": "", "after": "present"}, item in allow_add)
            continue
        if item not in after.rows:
            record({"item": item, "field": "__row_removed__", "before": "present", "after": ""}, item in allow_remove)
            continue
        before_row = before.rows[item]
        after_row = after.rows[item]
        for field in before.headers:
            old = before_row.get(field, "")
            new = after_row.get(field, "")
            if old == new:
                continue
            record({"item": item, "field": field, "before": old, "after": new}, (item, field) in authorized_fields)

    result = {
        "passed": not unauthorized,
        "changed_fields": changes,
        "unauthorized_changes": unauthorized,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not unauthorized else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(2)
