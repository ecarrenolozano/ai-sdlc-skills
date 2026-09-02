# Test Suite

The project uses pytest for all new Python and browser-driven tests. New `unittest.TestCase` tests are prohibited. pytest-bdd is configured for the later validation stage.

## Structure

- `unit/`: isolated technical or product units, organized to mirror `src/`.
- `integration/`: collaboration among real components, organized to mirror the primary source boundary under test.
- `regression/`: confirmed defect protection. Keep this category empty until a real defect exists, then place the regression where the defect is clearest.
- `validation/`: approved behavior scenarios using pytest-bdd.

## Fixtures

- module-only fixtures remain in the test module;
- directory-shared fixtures belong in that directory's `conftest.py`;
- suite-wide fixtures belong in `tests/conftest.py`.

## Commands

```bash
pytest tests/unit
pytest tests/integration
pytest tests/regression
pytest tests/validation
```

Regression and validation are intentionally empty in the technical foundation. Empty categories do not claim coverage.
