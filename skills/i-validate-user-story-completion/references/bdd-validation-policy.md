# BDD Validation Policy

## Scenario Mapping

Use approved acceptance criteria as the only source of expected behavior. For each selected story:

- copy the story identifier and title into the mapping evidence;
- list every approved scenario or criterion;
- map each criterion to one or more Gherkin scenarios;
- record `Blocked` for criteria that cannot be validated because implementation evidence or approved behavior is missing;
- do not create scenarios for unapproved edge cases, validation rules, user roles, persistence behavior, error payloads, or UI details.

Prefer one scenario per independently observable acceptance criterion. Combine criteria only when the approved wording describes one indivisible user outcome.

## Gherkin Style

Write features from the user's perspective:

```gherkin
Feature: <approved capability>

  Scenario: <approved observable outcome>
    Given <approved starting condition>
    When <approved user action or system event>
    Then <approved outcome>
```

Use `And` only to clarify the same step level. Keep scenario text close to approved acceptance criteria. Avoid implementation terms such as route names, classes, table names, fixtures, mocks, or adapters in `.feature` files.

## pytest-bdd Steps

Place step modules under `tests/validation/steps/`. Keep browser, API, database, or service fixtures in the smallest useful `conftest.py`.

Step definitions may use repository helpers and fixtures, but the step text must remain behavior-oriented. Prefer explicit assertions over broad snapshot checks. Do not skip or xfail scenarios to claim validation readiness.

## Evidence

Record:

- selected story IDs;
- approved criteria mapped;
- feature and step files changed;
- exact validation command;
- exit result;
- failing scenarios and likely owner when blocked;
- traceability fields changed.

Validation evidence belongs in normal test artifacts, the conversation, local status tracking, and version control history. Do not create persistent execution logs unless the project already has an approved tracker for them.
