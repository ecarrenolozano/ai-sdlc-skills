#!/usr/bin/env python3
"""Generate skill documentation from canonical skill directories."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DOCS_SKILLS_DIR = ROOT / "docs" / "skills"
REPO_URL = "https://github.com/ecarrenolozano/ai-sdlc-skills"


@dataclass(frozen=True)
class Skill:
    directory: Path
    name: str
    description: str
    body: str
    resource_counts: dict[str, int]

    @property
    def slug(self) -> str:
        return self.directory.name


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path} is missing YAML-style frontmatter")

    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path} has unsupported frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, text[match.end() :]


def count_files(directory: Path) -> int:
    if not directory.exists():
        return 0
    return sum(1 for path in directory.rglob("*") if path.is_file() and not is_ignored_generated_file(path))


def read_skills() -> list[Skill]:
    skills: list[Skill] = []
    for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            raise ValueError(f"{skill_dir} does not contain SKILL.md")
        frontmatter, body = parse_frontmatter(skill_file)
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if not name:
            raise ValueError(f"{skill_file} frontmatter is missing name")
        if not description:
            raise ValueError(f"{skill_file} frontmatter is missing description")
        if name != skill_dir.name:
            raise ValueError(f"{skill_file} name {name!r} does not match directory {skill_dir.name!r}")
        skills.append(
            Skill(
                directory=skill_dir,
                name=name,
                description=description,
                body=body.rstrip() + "\n",
                resource_counts={
                    "agents": count_files(skill_dir / "agents"),
                    "assets": count_files(skill_dir / "assets"),
                    "references": count_files(skill_dir / "references"),
                    "scripts": count_files(skill_dir / "scripts"),
                },
            )
        )
    return skills


def relative_repo_link(path: Path) -> str:
    path_type = "tree" if path.is_dir() else "blob"
    return f"{REPO_URL}/{path_type}/main/{path.relative_to(ROOT).as_posix()}"


def docs_link_for_source(path: Path) -> str:
    return relative_repo_link(path)


def list_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(path for path in directory.rglob("*") if path.is_file() and not is_ignored_generated_file(path))


def is_ignored_generated_file(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}


def markdown_file_list(title: str, files: list[Path], base_dir: Path) -> str:
    lines = [f"## {title}", ""]
    if not files:
        lines.extend(["No files.", ""])
        return "\n".join(lines)

    for path in files:
        label = path.relative_to(base_dir).as_posix()
        lines.append(f"- [{label}]({docs_link_for_source(path)})")
    lines.append("")
    return "\n".join(lines)


def demote_headings(markdown: str, levels: int = 1) -> str:
    prefix = "#" * levels
    lines: list[str] = []
    for line in markdown.splitlines():
        if re.match(r"^#{1,6}\s", line):
            lines.append(f"{prefix}{line}")
        else:
            lines.append(line)
    return "\n".join(lines)


def choose_process_flowchart(skill_dir: Path) -> tuple[Path | None, list[Path]]:
    candidates = [
        skill_dir / "references" / "process_flowchart.md",
        skill_dir / "references" / "process-flowchart.md",
    ]
    existing = [path for path in candidates if path.exists()]
    return (existing[0] if existing else None), existing


def build_skill_page(skill: Skill) -> str:
    skill_dir = skill.directory
    process_file, process_files = choose_process_flowchart(skill_dir)
    scripts = list_files(skill_dir / "scripts")
    references = list_files(skill_dir / "references")
    agents = list_files(skill_dir / "agents")
    assets = list_files(skill_dir / "assets")
    golden_examples = [path for path in references if "/golden-example/" in path.as_posix()]

    lines = [
        f"# {skill.name}",
        "",
        "<!-- Generated by scripts/generate_docs.py. Do not edit by hand. -->",
        "",
        "## Summary",
        "",
        skill.description,
        "",
        "## Repository Source",
        "",
        f"- [Canonical SKILL.md]({docs_link_for_source(skill_dir / 'SKILL.md')})",
        f"- [Skill directory]({docs_link_for_source(skill_dir)})",
        "",
        "## Resource Overview",
        "",
        "| Resource type | Files |",
        "| --- | ---: |",
    ]
    for resource_type in ("agents", "references", "scripts", "assets"):
        lines.append(f"| {resource_type} | {skill.resource_counts[resource_type]} |")
    lines.append("")

    lines.extend(["## Operating Process", ""])
    if process_file:
        if len(process_files) > 1:
            lines.extend(
                [
                    "Multiple process flowchart files exist. The documentation renders `references/process_flowchart.md` first.",
                    "",
                ]
            )
        lines.extend(
            [
                f"Source: [{process_file.relative_to(skill_dir).as_posix()}]({docs_link_for_source(process_file)})",
                "",
                demote_headings(process_file.read_text(encoding="utf-8").rstrip()),
                "",
            ]
        )
    else:
        lines.extend(["No process flowchart file was found for this skill.", ""])

    lines.append(markdown_file_list("Validation Scripts", scripts, skill_dir).rstrip())
    lines.append("")
    lines.append(markdown_file_list("Reference Material", references, skill_dir).rstrip())
    lines.append("")
    lines.append(markdown_file_list("Agent Configuration", agents, skill_dir).rstrip())
    lines.append("")
    lines.append(markdown_file_list("Assets", assets, skill_dir).rstrip())
    lines.append("")
    lines.append(markdown_file_list("Golden Examples", golden_examples, skill_dir).rstrip())
    lines.append("")
    lines.extend(
        [
            "## Canonical Skill Definition",
            "",
            "The following section is generated from the canonical `SKILL.md` body.",
            "",
            demote_headings(skill.body.rstrip()),
            "",
        ]
    )
    return "\n".join(lines)


def build_index(skills: list[Skill]) -> str:
    lines = [
        "# Skill Catalog",
        "",
        "<!-- Generated by scripts/generate_docs.py. Do not edit by hand. -->",
        "",
        "This catalog is generated from `skills/*/SKILL.md` frontmatter and each skill directory.",
        "",
        "## Skills",
        "",
        "| Skill | References | Scripts | Assets | Agents |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for skill in skills:
        lines.append(
            f"| [{skill.name}]({skill.slug}.md) | "
            f"{skill.resource_counts['references']} | "
            f"{skill.resource_counts['scripts']} | "
            f"{skill.resource_counts['assets']} | "
            f"{skill.resource_counts['agents']} |"
        )

    lines.extend(["", "## Descriptions", ""])
    for skill in skills:
        lines.extend([f"### [{skill.name}]({skill.slug}.md)", "", skill.description, ""])
    return "\n".join(lines)


def expected_outputs(skills: list[Skill]) -> dict[Path, str]:
    outputs = {DOCS_SKILLS_DIR / "index.md": build_index(skills)}
    for skill in skills:
        outputs[DOCS_SKILLS_DIR / f"{skill.slug}.md"] = build_skill_page(skill)
    return outputs


def check_outputs(outputs: dict[Path, str]) -> int:
    failures = 0
    expected_paths = set(outputs)
    for stale in DOCS_SKILLS_DIR.glob("*.md"):
        if stale not in expected_paths:
            failures += 1
            print(f"Stale generated docs file should be removed: {stale.relative_to(ROOT)}", file=sys.stderr)

    for path, expected in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != expected:
            failures += 1
            print(f"Generated docs are stale: {path.relative_to(ROOT)}", file=sys.stderr)
            diff = difflib.unified_diff(
                current.splitlines(),
                expected.splitlines(),
                fromfile=f"current/{path.relative_to(ROOT)}",
                tofile=f"expected/{path.relative_to(ROOT)}",
                lineterm="",
            )
            for line in list(diff)[:120]:
                print(line, file=sys.stderr)
    return failures


def write_outputs(outputs: dict[Path, str]) -> None:
    DOCS_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    expected_paths = set(outputs)
    for stale in DOCS_SKILLS_DIR.glob("*.md"):
        if stale not in expected_paths:
            stale.unlink()
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated docs are stale")
    args = parser.parse_args()

    skills = read_skills()
    outputs = expected_outputs(skills)
    if args.check:
        failures = check_outputs(outputs)
        if failures:
            print(f"{failures} generated documentation file(s) are stale.", file=sys.stderr)
            return 1
        print("Generated skill documentation is up to date.")
        return 0

    write_outputs(outputs)
    print(f"Generated documentation for {len(skills)} skills in {DOCS_SKILLS_DIR.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
