# Test Placement

## Unit

Use `tests/unit/` for isolated domain rules, values, functions, validators, configuration, and services with substituted boundaries.

## Integration

Use `tests/integration/` for real collaboration among Flask, application services, persistence adapters, SQLite, filesystem, processes, or HTTP contracts.

## Regression

Use `tests/regression/unit/` or `tests/regression/integration/` only for a confirmed defect. Include the issue or defect context in the module docstring and apply both `pytest.mark.regression` and the level marker.

## Validation

Reserve `tests/validation/features/` and `tests/validation/steps/` for approved product validation through `pytest-bdd`. Normal issue implementation should not create Gherkin scenarios unless the selected work explicitly belongs to validation.

## Fixtures

- module-only fixture -> test module;
- directory-shared fixture -> local `conftest.py`;
- suite-wide fixture -> `tests/conftest.py`.

## Avoid duplication

Do not repeat the same behavior at every level. Add broader tests when they prove a different risk, such as serialization, persistence, routing, or browser interaction.
