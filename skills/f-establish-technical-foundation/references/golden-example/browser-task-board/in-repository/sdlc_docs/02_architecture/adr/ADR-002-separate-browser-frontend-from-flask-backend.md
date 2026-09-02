# ADR-002: Separate the Browser Frontend from the Flask Backend

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision owners:** Edwin Carreno, SSC Developer
- **Related capabilities:** CAP-001 through CAP-006
- **Affected architecture elements:** Browser Frontend; Flask Backend; HTTP/JSON API boundary; Board Repository Port; SQLite Persistence Adapter; Persistence Mechanism

## Context

The approved product remains a single-user browser task board. The approved requirements define task creation, movement, editing, deletion, restoration, and task-status counts. They do not approve authentication, collaboration, or cross-device synchronization.

The previous architecture baseline selected a browser-only application with browser-local persistence. The revised architectural direction requires a web application with clearly separated frontend and backend components. The frontend uses HTML, CSS, and JavaScript. The backend uses Python and Flask. Product and business logic should live primarily in Python. The components communicate only through an explicit HTTP/JSON API and should be separable enough that either component can later move to a separate repository without a major rewrite.

Persistence was explicitly selected by Edwin Carreno on 2026-07-27: use SQLite backend persistence for the first release.

## Decision Drivers

- Keep approved task-board behavior intact.
- Establish a clear frontend/backend ownership boundary.
- Put product and business logic primarily in Python.
- Make frontend code reviewable, testable, and owned even when AI-assisted.
- Avoid implementation imports across the frontend/backend boundary.
- Preserve future repository separation and independent testability.
- Preserve board state with an approved backend persistence mechanism.

## Considered Options

| Option | Decision |
|---|---|
| Continue with the browser-only architecture from ADR-001 | Rejected because it conflicts with the required Flask backend and HTTP/JSON API boundary. |
| Add Flask while allowing frontend/backend source-code imports | Rejected because it prevents clean ownership and future repository separation. |
| Separate Browser Frontend and Flask Backend with HTTP/JSON only | Accepted because it satisfies the new architecture direction while preserving approved product behavior. |
| Select SQLite persistence now | Accepted because it provides durable single-user backend-owned persistence for US-0005. |
| Use Flask-managed session persistence now | Rejected because session lifecycle and size constraints make saved-board behavior less explicit. |

## Decision

Separate the product into two internal C4 containers:

- **Browser Frontend:** HTML, CSS, and JavaScript user interface.
- **Flask Backend:** Python service exposing the HTTP/JSON API and owning product logic.

The only allowed runtime dependency from frontend to backend is the documented HTTP/JSON API. The frontend must not import backend implementation code. The backend must not depend on frontend JavaScript modules.

The backend owns task-board product behavior, validation, status transitions, status-count derivation, and persistence coordination. Persistence is accessed through a backend-owned repository port implemented by a SQLite persistence adapter for the first release.

Frontend and backend must have separate dependencies, tests, documentation, and development commands. They may initially deploy together, but should remain structured as potentially independent deployable units. The SQLite database remains a backend-owned runtime concern and must not be accessed directly by the frontend.

## Consequences

### Positive

- Establishes a clear client-server architecture.
- Keeps product logic primarily in Python.
- Supports independent frontend and backend testing.
- Makes future repository separation feasible.
- Avoids treating AI-generated frontend code as unmanaged prototype code.

### Negative

- Adds more moving parts than the browser-only baseline.
- Requires API-contract design before implementation.
- Requires local development coordination between frontend and backend.
- SQLite adds local data-file, migration, backup, and reset considerations.

### Risks

- Frontend implementation could duplicate backend product logic.
- API contract drift could break integration.
- A joint initial deployment could hide accidental coupling.
- SQLite data-file handling could be underdocumented during local development or deployment.

## Validation

- Structurizr Container view shows Browser Frontend and Flask Backend as separate containers.
- Structurizr Component view shows backend API routes, task application service, repository port, SQLite persistence adapter, and status counter.
- Architecture documentation states the dependency rule: `Frontend -> HTTP/JSON API -> Backend`.
- Requirements-to-Architecture Coverage maps CAP-001 through CAP-006 to the revised containers.
- CAP-005 maps to the Board Repository Port, SQLite Persistence Adapter, and Persistence Mechanism.
- Technical foundation must add separate frontend and backend test/development commands.

## Supersedes

- ADR-001 for future implementation work, once this ADR is approved.

## Superseded By

None.
