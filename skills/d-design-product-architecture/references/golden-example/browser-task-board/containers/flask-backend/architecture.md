# Flask Backend Architecture

- **Structurizr container identifier:** flaskBackend
- **Container folder:** flask-backend
- **Decision status:** Confirmed architect decision
- **Evidence basis:** Approved Project Context; REQ-0001; CAP-001 through CAP-006; ADR-002

## Container Identity

Flask Backend is the Python service that exposes the Browser Task Board HTTP/JSON API.

## Purpose

Own product and business logic for the approved task-board behavior, coordinate persistence, and provide board state to the Browser Frontend.

## Responsibilities

- Expose explicit HTTP/JSON API routes for board and task operations.
- Validate approved task fields, including required title.
- Apply create, move, edit, and delete behavior.
- Derive pending, current, and completed counts.
- Load and save board state through a backend-owned persistence port implemented with SQLite.
- Keep backend dependencies, tests, README, and development command separate from frontend tooling.

## Covered Capabilities and Stories

| Capability | Story | Responsibility |
|---|---|---|
| CAP-001 | US-0001 | Create a task in TODO with approved task fields. |
| CAP-002 | US-0002 | Move a task among TODO, DOING, and DONE. |
| CAP-003 | US-0003 | Edit approved task fields. |
| CAP-004 | US-0004 | Delete a task. |
| CAP-005 | US-0005 | Restore saved board state through the selected persistence adapter. |
| CAP-006 | US-0006 | Return mapped pending, current, and completed counts. |

## Interfaces Provided

HTTP/JSON API consumed by the Browser Frontend. Exact routes and schemas are technical-foundation outputs after architecture approval.

## Interfaces Consumed

SQLite, accessed by the SQLite Persistence Adapter that implements the Board Repository Port.

## Data Ownership

The backend owns the task collection, task state transitions, status-count derivation, and persistence coordination. SQLite owns durable storage according to the approved strategy.

## Dependencies

- Python runtime.
- Flask.
- SQLite.

## Internal Building Blocks

| Building block | Type | Responsibility |
|---|---|---|
| API Routes | Component | Receive HTTP/JSON requests and return JSON responses. |
| Task Application Service | Component | Apply approved task-board behavior and validation. |
| Board Repository Port | Boundary | Define backend load/save operations independently of the selected storage. |
| SQLite Persistence Adapter | Component | Implement the repository port with SQLite. |
| Status Counter | Component | Derive pending, current, and completed counts. |

The internal structure is visible in Structurizr view `FlaskBackendComponents`.

## Runtime Responsibilities

The backend receives each task-board request, applies approved product behavior, persists resulting board state when needed, derives counts, and returns the current board representation as JSON.

## Quality Attributes

- Keep product behavior primarily in Python.
- Keep API behavior testable without browser UI tests.
- Keep SQLite isolated behind the repository port.

## Constraints

- Do not depend on frontend JavaScript modules.
- Do not expose behavior beyond approved Product Requirements.
- Do not add authentication, collaboration, or cross-device synchronization in the initial release.
- For the first release, bind only to `127.0.0.1`.
- Serve the frontend and API from the same local origin.
- Do not expose the Flask Backend as a remotely accessible hosted service without a later approved authentication, data-isolation, and operations decision.

## Related ADR

- [ADR-002: Separate the Browser Frontend from the Flask Backend](../../adr/ADR-002-separate-browser-frontend-from-flask-backend.md)

## Open Decisions

Exact route paths, JSON schemas, backend source-code layout, SQLite schema, and database file location remain technical-foundation decisions.
