# Authoring Skills

Each skill lives in its own directory under `skills/` and uses `SKILL.md` as its entry point.

## Expected Structure

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
├── assets/
├── references/
└── scripts/
```

Only `SKILL.md` is required. The other directories are added when the skill needs provider configuration, reusable templates, reference material, deterministic validators, or golden examples.

## Skill Page Generation

Run the generator after editing a skill:

```bash
python3 scripts/generate_docs.py
```

To verify that generated documentation is current:

```bash
python3 scripts/generate_docs.py --check
```

The generated files under `docs/skills/` are review artifacts. They should change when the canonical skill definition, process flowchart, validators, references, assets, or examples change.

## Frontmatter

Every `SKILL.md` must start with frontmatter:

```markdown
---
name: example-skill
description: Use when ...
---
```

The `name` should match the skill directory name. The `description` should explain when the skill applies, what it produces, and what it must not do.

## Process Flowcharts

When a skill has a process diagram, store it in `references/process_flowchart.md`. Some existing skills also contain `references/process-flowchart.md`; generated docs prefer `process_flowchart.md` and report both when both files exist.
