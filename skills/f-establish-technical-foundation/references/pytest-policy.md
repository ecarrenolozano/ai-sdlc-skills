# Pytest Policy

## Frameworks

- Use pytest for new Python tests.
- Configure pytest-bdd for later validation scenarios.
- Do not use `unittest.TestCase` as the project testing style.
- Allow `unittest.mock` only as a helper when justified.

## Directory categories

```text
tests/
├── unit/
├── integration/
├── regression/
└── validation/
    ├── features/
    └── steps/
```

- Unit tests isolate one unit or rule.
- Integration tests exercise collaboration among real components.
- Regression tests reproduce confirmed defects. Create `unit/` or `integration/` subdivisions only when a real defect requires them.
- Validation tests use pytest-bdd for approved behavior scenarios in a later workflow.

## Fixtures

- Keep module-only fixtures in the test module.
- Put directory-shared fixtures in that directory's `conftest.py`.
- Put suite-wide fixtures in `tests/conftest.py`.
- Prefer explicit fixtures and isolated temporary resources.

## Module organization

Use the templates as a navigation aid:

- module docstring;
- standard-library, third-party, and local imports;
- fixtures and setup;
- class groups when useful;
- nominal, negative, edge, or regression sections only when applicable.

Do not duplicate the same test as both a method and a free function. Do not keep unused sections merely to match a template. Let Ruff and human review handle general style rather than enforcing decorative comments through a complex validator.

## Foundation boundary

During foundation establishment, write only technical smoke tests such as importing the application factory, checking loopback defaults, or confirming configuration. Do not implement or validate product stories.
