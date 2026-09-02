# Browser Frontend Architecture

- **Structurizr container identifier:** browserFrontend
- **Container folder:** browser-frontend
- **Decision status:** Confirmed architect decision
- **Evidence basis:** Approved Project Context; REQ-0001; CAP-001 through CAP-006; ADR-002

## Container Identity

Browser Frontend is the HTML, CSS, and JavaScript application that runs in the user's browser.

## Purpose

Provide the approved task-board user interface and communicate with the Flask Backend only through the documented same-origin local HTTP/JSON API.

## Responsibilities

- Display TODO, DOING, and DONE board sections.
- Display task titles, optional descriptions, and mapped status counts returned by the backend.
- Capture create, move, edit, and delete user interactions.
- Send API requests to the Flask Backend.
- Render backend responses without duplicating product rules.
- Keep frontend dependencies, tests, README, and development command separate from the backend.

## Interfaces Provided

A browser user interface for the Task-board user.

## Interfaces Consumed

Same-origin local HTTP/JSON API provided by the Flask Backend.

## Data Ownership

The frontend owns transient UI state only. Durable board state and product logic belong to the Flask Backend.

## Dependencies

- A modern web browser.
- The Flask Backend API.
- Frontend tooling selected during technical foundation, if any.

## Internal Building Blocks

| Building block | Type | Responsibility |
|---|---|---|
| Board View | Component | Render board sections, tasks, forms, and counts. |
| Interaction Controller | Component | Translate user actions into API client calls. |
| API Client | Boundary | Own HTTP/JSON request and response handling. |

## Runtime Responsibilities

On startup, the frontend requests the current board from the backend. After user actions, it sends an HTTP/JSON request and redraws the board from the backend response.

## Quality Attributes

- Keep AI-assisted code reviewable and testable.
- Avoid duplicating backend-owned product logic.
- Keep frontend setup and tests independent from backend internals.

## Constraints

- Do not import backend implementation code.
- Do not access backend storage directly.
- Call the backend only through the same local origin served by Flask for the first release.
- Do not create unapproved authentication, collaboration, or cross-device behavior.

## Related ADR

- [ADR-002: Separate the Browser Frontend from the Flask Backend](../../adr/ADR-002-separate-browser-frontend-from-flask-backend.md)

## Open Decisions

Frontend test tooling and exact source-code layout remain technical-foundation decisions.
