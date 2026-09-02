#!/usr/bin/env python3
"""Inspect a repository technical foundation without modifying it."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tomllib
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def read_toml(path: Path) -> dict[str, object]:
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def requirement_name(requirement: object) -> str | None:
    if not isinstance(requirement, str):
        return None
    text = requirement.strip()
    if not text:
        return None
    text = text.split(";", 1)[0].strip()
    for separator in ("[", "<", ">", "=", "!", "~", " "):
        if separator in text:
            text = text.split(separator, 1)[0].strip()
    return text or None


def normalized_dependencies(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    names = [name for value in values if (name := requirement_name(value))]
    return sorted(set(names), key=str.lower)


def dependency_groups(pyproject: dict[str, object]) -> dict[str, object]:
    project = pyproject.get("project") if isinstance(pyproject.get("project"), dict) else {}
    build_system = (
        pyproject.get("build-system") if isinstance(pyproject.get("build-system"), dict) else {}
    )
    raw_groups = (
        pyproject.get("dependency-groups")
        if isinstance(pyproject.get("dependency-groups"), dict)
        else {}
    )
    optional = (
        project.get("optional-dependencies")
        if isinstance(project.get("optional-dependencies"), dict)
        else {}
    )

    development_names = {"dev", "develop", "development", "test", "tests", "quality", "lint"}
    documentation_names = {"doc", "docs", "documentation"}
    grouped = {
        "runtime_dependencies": normalized_dependencies(project.get("dependencies")),
        "development_dependencies": [],
        "documentation_dependencies": [],
        "build_system_dependencies": normalized_dependencies(build_system.get("requires")),
        "other_dependency_groups": {},
        "optional_dependencies": {},
    }

    for group_name, values in sorted(raw_groups.items()):
        names = normalized_dependencies(values)
        lowered = group_name.lower()
        if lowered in development_names:
            grouped["development_dependencies"].extend(names)
        elif lowered in documentation_names:
            grouped["documentation_dependencies"].extend(names)
        else:
            grouped["other_dependency_groups"][group_name] = names

    for group_name, values in sorted(optional.items()):
        grouped["optional_dependencies"][group_name] = normalized_dependencies(values)

    grouped["development_dependencies"] = sorted(
        set(grouped["development_dependencies"]), key=str.lower
    )
    grouped["documentation_dependencies"] = sorted(
        set(grouped["documentation_dependencies"]), key=str.lower
    )
    return grouped


def git_status(root: Path) -> dict[str, object]:
    if not (root / ".git").exists():
        return {"available": False, "entries": []}
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "available": True,
        "exit_code": completed.returncode,
        "entries": [line for line in completed.stdout.splitlines() if line.strip()],
        "stderr": completed.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.repository.resolve()

    pyproject = root / "pyproject.toml"
    pyproject_text = read_text(pyproject)
    pyproject_data = read_toml(pyproject)
    dependencies = dependency_groups(pyproject_data)
    all_dependency_names = sorted(
        {
            *dependencies["runtime_dependencies"],
            *dependencies["development_dependencies"],
            *dependencies["documentation_dependencies"],
            *dependencies["build_system_dependencies"],
            *[
                name
                for names in dependencies["other_dependency_groups"].values()
                for name in names
            ],
            *[
                name
                for names in dependencies["optional_dependencies"].values()
                for name in names
            ],
        },
        key=str.lower,
    )

    test_files = sorted(
        str(path.relative_to(root))
        for path in (root / "tests").rglob("test_*.py")
    ) if (root / "tests").is_dir() else []
    feature_files = sorted(
        str(path.relative_to(root))
        for path in (root / "tests").rglob("*.feature")
    ) if (root / "tests").is_dir() else []

    workflows = sorted(
        str(path.relative_to(root))
        for path in (root / ".github" / "workflows").glob("*.y*ml")
    ) if (root / ".github" / "workflows").is_dir() else []

    source_roots = [
        str(path.relative_to(root))
        for path in [root / "src", root / "frontend", root / "backend"]
        if path.exists()
    ]

    result = {
        "passed": root.is_dir(),
        "repository": str(root),
        "manifests": [name for name in ["pyproject.toml", "package.json", "requirements.txt", "uv.lock", "poetry.lock"] if (root / name).exists()],
        "source_roots": source_roots,
        "test_root_exists": (root / "tests").is_dir(),
        "test_directories": [
            name for name in ["unit", "integration", "regression", "validation"]
            if (root / "tests" / name).is_dir()
        ],
        "test_files": test_files,
        "feature_files": feature_files,
        "dependencies": dependencies,
        "dependencies_detected": all_dependency_names,
        "pytest_declared": "pytest" in all_dependency_names,
        "pytest_bdd_declared": "pytest-bdd" in all_dependency_names,
        "unittest_testcase_occurrences": [],
        "workflow_files": workflows,
        "development_docs": [name for name in ["README.md", "docs/development.md", "tests/README.md"] if (root / name).exists()],
        "git": git_status(root),
    }

    if (root / "tests").is_dir():
        for path in (root / "tests").rglob("*.py"):
            text = read_text(path)
            if re.search(r"\bunittest\.TestCase\b|\bfrom\s+unittest\s+import\s+TestCase\b", text):
                result["unittest_testcase_occurrences"].append(str(path.relative_to(root)))

    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
