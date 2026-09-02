# Development

## Install

```bash
uv sync --locked --all-groups
```

Use `uv lock` followed by `uv sync --all-groups` only for a deliberate dependency update.

## Run from the Repository Checkout

```bash
uv run python -m todo_board_ssc.backend
```

The default host is `127.0.0.1`. The repository checkout contains both the frontend and backend source roots.

## Tests

```bash
uv run pytest --collect-only
uv run pytest tests/unit
uv run pytest tests/integration
```

The regression and validation directories remain empty until a confirmed defect or approved validation scenario exists.

## Quality

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv build
```

`uv build` validates the Python package only. It is not the complete browser-application artifact.
