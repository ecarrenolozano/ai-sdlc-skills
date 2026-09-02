# Technical Foundation Proposal

## Repository

Browser Task Board after approved architecture and repository preparation.

## Approved Constraints

- Python and Flask backend.
- HTML, CSS, and JavaScript frontend.
- Same local origin.
- Default host `127.0.0.1`.
- SQLite remains behind the approved persistence boundary for later implementation.
- No product user-story implementation during foundation work.

## Proposed Changes

- Retain `pyproject.toml`, uv, and the `src/` layout.
- Add Flask, pytest, pytest-bdd, and concise pytest configuration.
- Add `frontend/` as the approved browser source root.
- Add a minimal Flask application factory and loopback runtime setting.
- Add the four primary test categories.
- Add technical smoke tests only.
- Add developer documentation and minimal CI.
- Use `uv sync --locked --all-groups` for reproducible installation.
- Document checkout-based local execution: the repository checkout is the application workspace, while `uv build` validates only the Python package.
- Set Technical foundation to `Pending Approval` after successful validation.

## Out of Scope

- No task entities.
- No product API routes.
- No SQLite product schema.
- No create, move, edit, delete, persistence, or count behavior.
- No product BDD scenarios.
- No GitHub changes.
