# TDD Execution

Ping-Pong roles:

- Tester driver proposed the failing tests that define each accepted behavior.
- Developer navigator implemented only after each meaningful RED, with the minimum code needed to pass the current Tester driver test.

## Cycle 1 - Create a valid task in TODO

User-visible status:

- Proposed test: Tester driver proposed `test_valid_title_creates_task_in_todo`.
- Created test: `tests/unit/todo_board_ssc/domain/test_task.py`.
- Current status: RED after the target test failed for missing task creation behavior.
- Developer navigator status: waiting; no production code is allowed until RED is confirmed.

RED:

```text
pytest tests/unit/todo_board_ssc/domain/test_task.py::TestTaskCreation::test_valid_title_creates_task_in_todo
FAILED: Task does not exist
```

GREEN:

```text
pytest tests/unit/todo_board_ssc/domain/test_task.py::TestTaskCreation::test_valid_title_creates_task_in_todo
PASSED
```

User-visible status:

- Current status: GREEN after the target test passed with the minimal task creation code.
- Developer navigator response: added only the task creation behavior required by the current RED test.

REFACTOR:

- Extracted the status value into the approved domain representation.
- Re-ran the module: passed.

User-visible status:

- Current status: REFACTOR complete; target tests stayed green.

## Cycle 2 - Reject a blank title

User-visible status:

- Proposed test: Tester driver proposed `test_blank_title_is_rejected`.
- Created test: `tests/unit/todo_board_ssc/domain/test_task.py`.
- Current status: RED after the target test failed because blank titles were accepted.
- Developer navigator status: waiting; no validation code is allowed until RED is confirmed.

RED:

```text
pytest tests/unit/todo_board_ssc/domain/test_task.py::TestTaskCreation::test_blank_title_is_rejected
FAILED: blank title was accepted
```

GREEN:

```text
pytest tests/unit/todo_board_ssc/domain/test_task.py::TestTaskCreation::test_blank_title_is_rejected
PASSED
```

User-visible status:

- Current status: GREEN after title validation passed the target test.
- Developer navigator response: added only title normalization and blank-title rejection for the current RED test.

REFACTOR:

- Centralized title normalization.
- Re-ran the unit module: passed.

User-visible status:

- Current status: REFACTOR complete; unit tests stayed green.

## Cycle 3 - Expose creation through the approved API boundary

User-visible status:

- Proposed test: Tester driver proposed the create-task API integration test.
- Created test: `tests/integration/todo_board_ssc/backend/test_create_task.py`.
- Current status: RED after the Flask route returned 404.
- Developer navigator status: waiting; no route code is allowed until RED is confirmed.

RED:

```text
pytest tests/integration/todo_board_ssc/backend/test_create_task.py
FAILED: POST route returned 404
```

GREEN:

```text
pytest tests/integration/todo_board_ssc/backend/test_create_task.py
PASSED
```

User-visible status:

- Current status: GREEN after the route delegated to the application service and returned the expected JSON.
- Developer navigator response: added only the route/service collaboration needed for the current RED test.

REFACTOR:

- Kept route translation separate from the application service.
- Re-ran unit and integration tests: passed.

User-visible status:

- Current status: REFACTOR complete; unit and integration tests stayed green.
