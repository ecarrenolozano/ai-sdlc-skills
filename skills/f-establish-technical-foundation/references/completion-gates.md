# Completion Gates

The technical foundation may move to `Complete` only after all applicable gates pass.

## Approved scope

- Product Context, Product Requirements, Architecture, and Repository preparation are complete.
- No product behavior or architecture decision was silently added.

## Repository foundation

- Approved source boundaries exist.
- Dependency and lockfile strategy is reproducible.
- Local installation and run commands are documented.
- Checkout-based execution or another approved delivery convention is documented clearly.

## Testing

- pytest is declared and configured.
- pytest-bdd is declared and configured for later validation.
- `tests/unit`, `tests/integration`, `tests/regression`, and `tests/validation` exist.
- New tests do not use `unittest.TestCase`.
- Technical smoke tests pass.
- Empty future categories are reported honestly.

## Quality and CI

- Configured lint, format, type, coverage, and build checks pass when applicable.
- CI uses the same reproducible commands documented for developers.
- Generated local artifacts are ignored.

## Human control

- The final diff matches the approved proposal.
- No unapproved environment or remote action occurred.
- The user explicitly accepted the validated foundation.
