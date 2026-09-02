# Release

## Local Package Build

```bash
uv sync --locked --all-groups
uv build
```

## Local Container

```bash
podman build -t browser-task-board:local .
podman run --rm -p 127.0.0.1:5000:5000 browser-task-board:local
```

This example documents local execution only. Public hosting, registry publishing, and operational deployment require separate approval.
