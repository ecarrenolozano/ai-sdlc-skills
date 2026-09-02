# Release Deployment Proposal

## Scope

Prepare local release/deployment artifacts for a validated implementation.

## Proposed Local Changes

- Confirm `pyproject.toml` version remains `0.1.0` for the first local release candidate.
- Preserve `uv.lock`; no dependency change is proposed.
- Add a local-only `Containerfile` that binds the application to loopback inside the approved runtime model.
- Add `docs/release.md` with package build, local run, and local container commands.
- Update only the `Release deployment` trace row after validation.

## Commands

```bash
uv sync --locked --all-groups
uv run pytest
uv build
podman build -t browser-task-board:local .
python3 .agents/skills/j-prepare-release-deployment/scripts/validate_release_preparation.py . --require-trace
```

No tag, push, publish, registry upload, GitHub release, or hosted deployment is included.
