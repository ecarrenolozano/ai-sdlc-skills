#!/usr/bin/env python3
"""Validate release/deployment preparation artifacts without assuming a target."""
from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path
from typing import Any


TRACE_ROW_RE = re.compile(r"^\|\s*Release deployment\s*\|", re.MULTILINE)
PUBLIC_BIND_RE = re.compile(r"\b0\.0\.0\.0\b|--host\s+0\.0\.0\.0|host=['\"]0\.0\.0\.0")
SECRET_RE = re.compile(r"(password|token|secret|api_key)\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE)


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


def workflow_files(root: Path) -> list[Path]:
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return []
    return sorted([*directory.glob("*.yml"), *directory.glob("*.yaml")])


def container_files(root: Path) -> list[Path]:
    names = {"Dockerfile", "Containerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"}
    return sorted(path for path in root.rglob("*") if path.is_file() and path.name in names and ".git" not in path.parts)


def validate(root: Path, require_trace: bool) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    pyproject = load_pyproject(root / "pyproject.toml")
    version = None
    project = pyproject.get("project")
    if isinstance(project, dict):
        raw_version = project.get("version")
        if isinstance(raw_version, str):
            version = raw_version
    if (root / "pyproject.toml").exists() and not version:
        warnings.append("pyproject.toml exists but project.version was not found")

    lockfiles = [path.name for path in root.iterdir() if path.is_file() and path.name in {"uv.lock", "poetry.lock", "Pipfile.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"}]
    workflows = workflow_files(root)
    containers = container_files(root)

    docs_text = "\n".join(read_text(path) for path in [root / "README.md", *sorted((root / "docs").glob("*.md"))] if path.exists())
    if not docs_text.strip():
        warnings.append("release/deployment documentation was not found in README.md or docs/*.md")

    container_warnings: list[str] = []
    for path in containers:
        text = read_text(path)
        rel = str(path.relative_to(root))
        if PUBLIC_BIND_RE.search(text):
            container_warnings.append(f"public bind or host exposure requires approved architecture: {rel}")
        if SECRET_RE.search(text):
            errors.append(f"possible hardcoded secret in container file: {rel}")

    workflow_warnings: list[str] = []
    for path in workflows:
        text = read_text(path)
        rel = str(path.relative_to(root))
        if SECRET_RE.search(text):
            errors.append(f"possible hardcoded secret in workflow: {rel}")
        if "docker push" in text or "podman push" in text or "gh release create" in text:
            workflow_warnings.append(f"publishing command found; verify separate approval: {rel}")

    trace = root / "sdlc_docs" / "trace_workflow.md"
    trace_present = trace.is_file()
    trace_has_row = False
    if trace_present:
        trace_has_row = TRACE_ROW_RE.search(read_text(trace)) is not None
    if require_trace and not trace_present:
        errors.append("sdlc_docs/trace_workflow.md is required but missing")
    if require_trace and trace_present and not trace_has_row:
        errors.append("trace_workflow.md is missing Release deployment row")

    return {
        "passed": not errors,
        "repository": str(root),
        "version": version,
        "lockfiles": sorted(lockfiles),
        "workflow_files": [str(path.relative_to(root)) for path in workflows],
        "container_files": [str(path.relative_to(root)) for path in containers],
        "trace_workflow": {
            "exists": trace_present,
            "release_deployment_row": trace_has_row,
        },
        "errors": errors,
        "warnings": warnings + container_warnings + workflow_warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", type=Path)
    parser.add_argument("--require-trace", action="store_true")
    args = parser.parse_args()

    result = validate(args.repository, args.require_trace)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
