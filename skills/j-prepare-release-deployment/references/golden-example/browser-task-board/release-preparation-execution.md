# Release Preparation Execution

## Commands

```bash
uv sync --locked --all-groups
```

Result: passed.

```bash
uv run pytest
```

Result: passed.

```bash
uv build
```

Result: passed.

```bash
podman build -t browser-task-board:local .
```

Result: passed.

```bash
python3 .agents/skills/j-prepare-release-deployment/scripts/validate_release_preparation.py . --require-trace
```

Result: passed.

No remote release or deployment command was run.
