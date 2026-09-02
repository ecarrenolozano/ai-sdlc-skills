# Local Implementation Proposal

## Mode

Single issue implementation

## Selected Issue

`US-0001 - Create a task`

## Baseline

- Existing unit and integration tests pass.
- Technical foundation is `Complete`.
- No task-domain production code exists.

## Best-practice References

- `references/best-practices/README.md` read.
- `references/best-practices/python-best-practices.md` read for backend Python implementation and pytest guidance.

## Ping-Pong TDD Review

- Tester driver: define the intended logic with failing unit tests for valid task creation and blank-title rejection, then a failing integration test for `POST /api/tasks`.
- Developer navigator: respond only after meaningful RED with the minimum backend application/domain code and API route code needed to pass those tests.
- Reconciled decision: Tester driver creates the RED signal first; Developer navigator implements the GREEN response for that exact signal.

## Code-level Design

- Architecture elements: Browser Frontend, Flask Backend, API Routes, Task Application Service, Board Repository Port, SQLite Persistence Adapter.
- Planned backend code elements: task domain object or factory, create-task application service, API route handler for `POST /api/tasks`, repository port used at the backend boundary.
- Planned frontend code elements: no frontend implementation in this issue unless the selected issue proposal is expanded and approved.
- Central code-level index: create `sdlc_docs/02_architecture/code-level.md` with the US-0001 cross-container map and `POST /api/tasks` contract.
- Per-container code-level map: create `sdlc_docs/02_architecture/containers/flask-backend/code-level.md` with backend modules, route, service, repository port, and adapter responsibilities.
- Mermaid diagrams: include a `sequenceDiagram` for the create-task request and a `classDiagram` for backend service/port/adapter relationships.

## TDD Plan

1. Tester driver -> valid task creation and default `TODO` status -> unit test under `tests/unit/todo_board_ssc/domain/test_task.py` -> expected RED because task creation does not exist.
2. Developer navigator -> add the minimum task object/factory behavior needed for the RED test to pass.
3. Tester driver -> blank title rejection -> unit test in the same module -> expected RED because title validation does not exist.
4. Developer navigator -> add the minimum validation behavior needed for the RED test to pass.
5. Tester driver -> create-task application/API collaboration -> integration test under `tests/integration/todo_board_ssc/backend/test_create_task.py` -> expected RED because the route does not exist.
6. Developer navigator -> add the minimum route/service collaboration needed for the RED test to pass.

## User-visible TDD Status Plan

- Report Tester driver's proposed tests before approval.
- Report Developer navigator's implementation strategy before approval.
- Report each created test path and RED result.
- Report each GREEN result after implementation.
- Report each REFACTOR result after cleanup and rerun.

## Local Status-Tracking Plan

- Update `sdlc_docs/trace_workflow.md` after successful validation.
- Update `sdlc_docs/03_implementation/backlog_priority.md` after successful validation.
- Scope: Implementation row and implementation-owned backlog-priority status fields only.
- Implementation status: keep `In Progress` because additional approved issues remain after `US-0001`.
- Evidence to record: selected issue, unit/integration/quality command results, code-level docs created, remaining issue IDs, and next recommended issue from `sdlc_docs/03_implementation/backlog_priority.md`.
- Backlog-priority update: mark `US-0001` as locally implemented and refresh the next recommended issue.
- Earlier requirements, architecture, repository preparation, and technical foundation rows remain unchanged.

## Likely Files

Create:

- `src/todo_board_ssc/domain/task.py`
- `src/todo_board_ssc/application/create_task.py`
- `tests/unit/todo_board_ssc/domain/test_task.py`
- `tests/integration/todo_board_ssc/backend/test_create_task.py`

Modify only the approved Flask composition boundary required to expose the behavior.

## Dependencies

None.

## Out of Scope

- persistence schema beyond the minimum approved boundary;
- drag-and-drop, edit, delete, or counters;
- GitHub or version-control actions.
