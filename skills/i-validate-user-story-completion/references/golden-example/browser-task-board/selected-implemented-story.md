# Selected Implemented Story

- **Story:** US-0001 - Create a task
- **Implementation evidence:** Local implementation completed through `g-implement-repository-work`; unit and integration tests pass.
- **Approved acceptance criterion:**

```gherkin
Scenario: Create a task with a title
  Given the board is available
  When the user creates a task with a non-empty title
  Then the task is added to TODO with that title
```

- **Validation scope:** Confirm the approved behavior through BDD only.
- **Out of scope:** Editing tasks, deleting tasks, task movement, pull request creation, issue closure, and release deployment.
