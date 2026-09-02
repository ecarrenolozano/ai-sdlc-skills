# BDD Mapping

| Story | Approved criterion | Feature scenario | Status |
|---|---|---|---|
| US-0001 | Create a task with a title | `tests/validation/features/create_task.feature::Create a task with a title` | Mapped |

## Scenario

```gherkin
Feature: Create tasks

  Scenario: Create a task with a title
    Given the board is available
    When the user creates a task with a non-empty title
    Then the task is added to TODO with that title
```

No criteria remain unmapped.
