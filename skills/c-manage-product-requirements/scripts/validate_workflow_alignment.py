#!/usr/bin/env python3
"""Check that SKILL.md numbered workflow steps map one-to-one to Mermaid nodes."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def workflow_numbers(text: str) -> list[int]:
    match = re.search(r"(?ms)^## Workflow\s*$\n(.*?)(?=^##\s|\Z)", text)
    if not match:
        raise ValueError("SKILL.md has no ## Workflow section")
    return [int(n) for n in re.findall(r"(?m)^\s*(\d+)\.\s+", match.group(1))]


def flowchart_numbers(text: str) -> list[int]:
    blocks = re.findall(r"(?ms)```mermaid\s*(.*?)```", text)
    if not blocks:
        raise ValueError("Flowchart file has no Mermaid block")
    return [int(n) for n in re.findall(r"(?:\[|\{)(\d+)\.\s", "\n".join(blocks))]


def duplicates(values: list[int]) -> list[int]:
    return sorted({n for n in values if values.count(n) > 1})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", type=Path)
    parser.add_argument("flowchart", type=Path)
    args = parser.parse_args()

    skill_steps = workflow_numbers(args.skill.read_text(encoding="utf-8"))
    chart_steps = flowchart_numbers(args.flowchart.read_text(encoding="utf-8"))
    expected = list(range(1, max(skill_steps, default=0) + 1))
    result = {
        "passed": True,
        "workflow_steps": skill_steps,
        "flowchart_steps": chart_steps,
        "workflow_continuous": skill_steps == expected,
        "workflow_duplicates": duplicates(skill_steps),
        "flowchart_duplicates": duplicates(chart_steps),
        "missing_in_flowchart": sorted(set(skill_steps) - set(chart_steps)),
        "extra_in_flowchart": sorted(set(chart_steps) - set(skill_steps)),
    }
    result["passed"] = all([
        result["workflow_continuous"],
        not result["workflow_duplicates"],
        not result["flowchart_duplicates"],
        not result["missing_in_flowchart"],
        not result["extra_in_flowchart"],
    ])
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
