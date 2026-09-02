# Foundation Rules

## Keep the foundation minimal

Establish only infrastructure needed before the next approved implementation issue:

- approved source boundaries;
- dependency and lockfile management;
- local run commands;
- pytest and pytest-bdd;
- technical smoke tests;
- quality checks;
- minimal CI;
- concise developer documentation.

Do not create product modules, speculative abstractions, placeholder APIs, or fake validation scenarios.

## Prefer existing viable tools

Retain the repository's current package manager, build backend, test runner, and quality tools when they satisfy the approved architecture and constraints. Propose a replacement only when the current choice is unusable or contradictory.

## Separate durable decisions from operational evidence

Record durable setup instructions in `README.md`, `docs/development.md`, and `tests/README.md`. Keep command output and temporary comparison notes in the conversation rather than creating permanent reports.

## Protect human control

Require approval before local writes and separate approval before remote actions. Final validation does not authorize a commit, push, pull request, issue update, or workflow-state completion.

## Handle packaging pragmatically

For a local application explicitly run from a repository checkout, document that the wheel validates only the Python package. Do not block the entire foundation on producing a complete installable application artifact unless that artifact is part of the approved scope.

Route material delivery-architecture decisions to `d-design-product-architecture`.
