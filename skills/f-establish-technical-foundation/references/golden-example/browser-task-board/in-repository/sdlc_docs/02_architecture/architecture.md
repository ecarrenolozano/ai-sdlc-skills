# Browser Task Board Product Architecture

## Document Control

- **Project:** Browser Task Board
- **Architecture baseline:** ARCH-0002
- **Source Project Context:** `sdlc_docs/00_inception/project_context.md`
- **Source Product Requirements:** `sdlc_docs/01_requirements/product_requirements.md`
- **Last updated:** 2026-07-27
- **Architecture state:** Complete

## How to View This Architecture

The canonical architecture model is `sdlc_docs/02_architecture/diagrams/workspace.dsl`.

### Prerequisites

- Docker
- Docker Compose

### Start Structurizr

From the repository root:

```bash
docker compose -f sdlc_docs/02_architecture/diagrams/docker-compose.yml up
```

Open `http://localhost:8080`.

### Stop Structurizr

```bash
docker compose -f sdlc_docs/02_architecture/diagrams/docker-compose.yml down
```

### Exported Diagram Images

No exported image is currently included. The architect may export SVG or PNG files into `sdlc_docs/02_architecture/diagrams/images/` and add verified relative links to this document. `workspace.dsl` remains canonical.

## 1. Introduction and Goals

### 1.1 Requirements Overview

The approved initial release is a single-user browser task board. REQ-0001 and US-0001 through US-0006 define creation, movement, editing, deletion, restoration, and mapped status counts across TODO, DOING, and DONE.

This architecture changes the technical baseline from a browser-only application to a separated web application:

```text
Browser Frontend -> HTTP/JSON API -> Flask Backend -> Persistence mechanism
```

The architecture does not add authentication, collaboration, or cross-device synchronization to the first release.

### 1.2 Quality Goals

| Priority | Quality goal | Classification | Architectural relevance |
|---|---|---|---|
| 1 | Saved board continuity | Confirmed requirement | CAP-005 requires state restoration between browser sessions. |
| 2 | Frontend/backend separation | Confirmed architect decision | ADR-002 establishes an explicit HTTP/JSON boundary and prohibits source-code imports across it. |
| 3 | Product logic ownership | Confirmed architect decision | Task behavior and persistence coordination live primarily in Python in the Flask Backend. |
| 4 | Future repository separation | Confirmed architect decision | Separate dependencies, tests, documentation, and commands reduce the cost of moving either component later. |
| 5 | One-day deliverability awareness | Confirmed requirement | The Project Context requires a tightly bounded first release; the foundation should stay small. |

### 1.3 Stakeholders

| Stakeholder | Role | Architecture interest |
|---|---|---|
| Task-board user | Intended user | Use the approved personal task board in a browser. |
| Edwin Carreno | SSC Developer and architecture reviewer | Confirm scope fidelity, simplicity, traceability, and future evolution boundaries. |
| Future implementer | Developer or maintainer | Implement the frontend and backend without crossing ownership boundaries. |

## 2. Constraints

### 2.1 Technical Constraints

| Constraint | Classification | Evidence or decision |
|---|---|---|
| Run in a web browser | Confirmed requirement | Project Context, Section 13. |
| Preserve board state between browser sessions | Confirmed requirement | CAP-005 / US-0005. |
| Use an HTML, CSS, and JavaScript frontend | Confirmed architect decision | ADR-002. |
| Use a Python Flask backend | Confirmed architect decision | ADR-002. |
| Communicate only through explicit HTTP/JSON APIs | Confirmed architect decision | ADR-002. |
| Keep product and business logic primarily in Python | Confirmed architect decision | ADR-002. |
| Keep frontend and backend independently testable and documented | Confirmed architect decision | ADR-002. |
| Bind Flask Backend only to `127.0.0.1` for the first release | Confirmed architect decision | ADR-003. |
| Serve the frontend and API from the same local Flask origin | Confirmed architect decision | ADR-003. |
| Do not deploy the first release as a remotely accessible hosted Flask application | Confirmed architect decision | ADR-003; no approved authentication or collaboration scope. |
| Do not add authentication, collaboration, or cross-device synchronization | Confirmed requirement | Project Context exclusions and Product Requirements scope. |

### 2.2 Organizational Constraints

The frontend may be generated with substantial AI assistance, but generated code is production code: it must be reviewable, testable, and owned by the development team.

The first release deploys the frontend and backend together through one local Flask-served origin. The architecture still keeps frontend and backend source, tests, and responsibilities separate so they remain understandable and replaceable.

### 2.3 Conventions

- Structurizr DSL is canonical for C4 views.
- Internal container folders use normalized technical slugs.
- Architecture decisions are recorded under `sdlc_docs/02_architecture/adr/`.
- Exact source-code layout remains technical-foundation work, not product behavior.

## 3. Context and Scope

### 3.1 Business Context

**Structurizr view:** `SystemContext`

The Task-board user uses Browser Task Board in a browser to manage a personal board. No external user, identity provider, collaboration service, or cross-device synchronization service is part of the initial release.

| Communication partner | Input | Output |
|---|---|---|
| Task-board user | Approved task actions and task information | Board state, task details, and mapped counts |

### 3.2 Technical Context

The Browser Frontend presents the user interface and calls the Flask Backend over HTTP/JSON. The Flask Backend owns product behavior and persistence coordination. The Persistence Mechanism uses SQLite behind the backend persistence adapter.

The initial architecture has no frontend import of backend implementation modules and no backend dependency on frontend JavaScript modules.

## 4. Solution Strategy

Use two internal C4 containers:

- **Browser Frontend:** HTML, CSS, and JavaScript application responsible for rendering the board and translating user interactions into API calls.
- **Flask Backend:** Python service responsible for product logic, validation, status transitions, status counts, API responses, and persistence coordination.

Use a documented HTTP/JSON API as the only runtime dependency from frontend to backend. Keep frontend and backend dependencies, tests, READMEs, and development commands separate inside the repository so either component can later move to another repository without a major architectural rewrite.

Use SQLite backend persistence for the first release. The architecture keeps a backend persistence port so SQLite remains isolated from task behavior and can be reassessed in a later approved architecture change.

## 5. Building Block View

### 5.1 Whitebox Overall System

**Structurizr view:** `Containers`

| Container | Folder | Decision status | Responsibility |
|---|---|---|---|
| Browser Frontend | `containers/browser-frontend/` | Confirmed architect decision | Provide the approved browser UI and call the backend API. |
| Flask Backend | `containers/flask-backend/` | Confirmed architect decision | Own product logic, expose HTTP/JSON API, and coordinate persistence. |
| Persistence Mechanism | `containers/persistence-mechanism/` | Confirmed architect decision | Preserve board state using SQLite backend persistence. |

### 5.2 Level 2

**Structurizr view:** `FlaskBackendComponents`

The Flask Backend Component view shows the API routes, task application service, board repository port, SQLite persistence adapter, and status counter. It exists because ADR-002 depends on the frontend/backend boundary and backend persistence boundary.

Detailed responsibilities are documented in `containers/browser-frontend/architecture.md` and `containers/flask-backend/architecture.md`.

### 5.3 Level 3

No additional level-3 decomposition is required. Exact files, classes, route names, schemas, and test helpers belong to technical foundation and implementation planning after architecture approval.

## 6. Runtime View

| Scenario | Runtime responsibility |
|---|---|
| Create task, CAP-001 / US-0001 | Browser Frontend submits task information to the Flask Backend; the backend validates the title, creates the task in TODO, persists the resulting board state, and returns the updated board. |
| Move task, CAP-002 / US-0002 | Browser Frontend sends the requested status change; Flask Backend applies the transition, persists state, and returns the updated board. |
| Edit task, CAP-003 / US-0003 | Browser Frontend sends edited task fields; Flask Backend validates and persists the update. |
| Delete task, CAP-004 / US-0004 | Browser Frontend requests deletion; Flask Backend removes the task from the board state and persists the result. |
| Restore board, CAP-005 / US-0005 | Browser Frontend requests the board on startup; Flask Backend loads board state through the selected persistence adapter and returns it as JSON. |
| View counts, CAP-006 / US-0006 | Flask Backend derives pending, current, and completed counts from current task states and returns them with board state. |

## 7. Deployment View

**Structurizr view:** `Deployment`

The first release runs as a personal local web application on the user's machine. The Browser Frontend runs in the user's browser. The Flask Backend runs on the same machine and binds only to `127.0.0.1`. Flask serves both the frontend and API from the same local origin. The SQLite database is a personal local database owned by one local application instance.

A hosted remotely accessible Flask deployment is not part of the first release. Hosting the application remotely would require a later approved product and architecture change covering authentication, data isolation, HTTPS, operational ownership, backup/restore, and deployment monitoring.

| Deployment option | Decision | Consequence |
|---|---|---|
| Local Flask Backend bound to `127.0.0.1` with local SQLite | Selected | Matches the approved single-user, no-authentication release. |
| Hosted remotely accessible Flask application | Rejected for first release | Unsafe without authentication and operational controls; requires future approval. |

## 8. Crosscutting Concepts

| Concept | Classification | Evidence | Architecture approach |
|---|---|---|---|
| API boundary | Confirmed architect decision | ADR-002 | Frontend communicates with backend only through HTTP/JSON. |
| Product logic placement | Confirmed architect decision | ADR-002 | Flask Backend owns task behavior, validation, status transitions, counts, and persistence coordination. |
| Frontend ownership | Confirmed architect decision | ADR-002 | AI-assisted frontend code remains reviewable, testable, and team-owned. |
| Task-state model | Confirmed requirement | CAP-001 through CAP-004 | Backend state supports approved fields and TODO, DOING, DONE statuses. |
| Required title validation | Confirmed requirement | US-0001 | Backend validates required title before persistence. |
| Persistence | Confirmed architect decision | ADR-002; CAP-005 / US-0005; stakeholder persistence selection on 2026-07-27 | Backend uses a persistence port implemented by a SQLite adapter for the first release. |
| Deployment security | Confirmed architect decision | ADR-003 | The Flask Backend binds only to `127.0.0.1`; remote hosting is excluded for the first release. |
| Local server security model | Confirmed architect decision | ADR-003; Project Context exclusions | Loopback-only binding and same-origin local serving are the first-release security model; authentication is not required for the local personal instance. |

### Persistence Alternatives

| Alternative | Preserves approved observable behavior? | Impact |
|---|---|---|
| Browser-tab or purely in-memory state | No | Does not reliably satisfy return-after-browser-close behavior. |
| Flask-managed session | Maybe | Can preserve same-browser continuity, but lifecycle, size, and deployment behavior must be accepted. |
| Backend SQLite persistence | Selected | Strong fit for durable single-user state; adds a local data file and migration/backup concerns. |
| Cross-device backend persistence | More than required | Adds product behavior not approved for the first release unless explicitly scoped. |

## 9. Architectural Decisions

| ADR | Status | Summary | Affected elements |
|---|---|---|---|
| [ADR-001](adr/ADR-001-browser-local-persistence-boundary.md) | Superseded | Browser-local persistence behind Board State Repository for ARCH-0001. | Historical Browser Task Board App baseline |
| [ADR-002](adr/ADR-002-separate-browser-frontend-from-flask-backend.md) | Accepted | Separate the browser frontend from the Flask backend, communicate only through HTTP/JSON, and use SQLite backend persistence. | Browser Frontend; Flask Backend; API boundary; persistence port |
| [ADR-003](adr/ADR-003-localhost-only-personal-deployment.md) | Accepted | Run the first release as a localhost-only personal Flask application with local SQLite. | Browser Frontend; Flask Backend; Persistence Mechanism; Deployment view |

## 10. Quality Requirements

### 10.1 Quality Requirements Overview

The revised baseline prioritizes saved-state continuity, explicit frontend/backend separation, backend-owned product logic, and future separability. The first release remains intentionally single-user and excludes authentication, collaboration, and cross-device synchronization.

### 10.2 Quality Scenarios

| ID | Source and stimulus | Environment | Expected architecture response | Evidence or measure |
|---|---|---|---|---|
| Q-001 | The user returns after previously saving board changes | Same approved runtime context | Flask Backend loads saved state through the SQLite persistence adapter | CAP-005 / US-0005 is satisfied |
| Q-002 | Frontend implementation changes | Development | Backend tests and product logic remain unaffected except through API contract changes | Separate frontend/backend tests pass |
| Q-003 | Backend task logic changes | Development | Frontend remains coupled only to documented JSON contract | API contract tests identify intentional changes |
| Q-004 | A future repository split occurs | Repository evolution | Component-specific dependencies, tests, docs, and commands move with the component | No source-code imports cross the boundary |
| Q-005 | A future approved collaboration requirement arrives | Architecture evolution | Backend/API/persistence can be reassessed without moving product logic out of Python | New Product Requirements and architecture approval are required |
| Q-006 | A network client attempts to access the Flask Backend from another machine | First-release local runtime | The backend is not reachable because it binds only to `127.0.0.1` | ADR-003 is satisfied |

## 11. Risks and Technical Debt

| Type | Description | Impact | Mitigation or next action | Status |
|---|---|---|---|---|
| Risk | More moving parts than browser-only baseline | One-day delivery risk increases | Keep foundation minimal and avoid unapproved behavior | Accepted if architecture is approved |
| Risk | Frontend could duplicate product logic | Divergent behavior and weak ownership | Backend owns product rules; API responses include derived counts | Mitigation required |
| Risk | API contract drift | Frontend/backend integration failures | Add API/contract tests in technical foundation | Mitigation required |
| Risk | SQLite data file requires local operational care | Lost or misplaced database file can lose board state | Document local data path, backup expectations, and reset behavior during technical foundation | Mitigation required |
| Risk | Flask may be misconfigured to bind publicly | An unauthenticated API could be exposed | Document and test first-release bind address as `127.0.0.1` | Mitigation required |
| Technical debt | Initial joint deployment may hide separability problems | Future split becomes harder | Separate commands, dependencies, docs, and tests from the start | Mitigation required |
| Technical debt | Hosted deployment is deferred | Future remote access requires authentication and operations design | Re-enter product requirements and architecture before hosting remotely | Accepted |

## 12. Glossary

| Term | Meaning |
|---|---|
| Browser Frontend | HTML, CSS, and JavaScript user interface that runs in the user's browser. |
| Flask Backend | Python service that exposes the product HTTP/JSON API and owns task-board business logic. |
| API boundary | The only allowed runtime dependency from frontend to backend. |
| Persistence port | Backend-owned abstraction for saving and loading board state while isolating task behavior from SQLite. |
| Container | Independently executing application or data store in the C4 model. |

# Workflow Extensions

## Architecture Element Register

| Element ID | Type | Name | Evidence IDs | Decision status | ADR or open decision |
|---|---|---|---|---|---|
| AE-001 | Software System | Browser Task Board | REQ-0001 | Confirmed requirement | None |
| AE-002 | Container | Browser Frontend | CAP-001 through CAP-006 | Confirmed architect decision | ADR-002 |
| AE-003 | Container | Flask Backend | CAP-001 through CAP-006 | Confirmed architect decision | ADR-002 |
| AE-004 | Component | Frontend API Client | CAP-001 through CAP-006 | Internal architecture constraint | ADR-002 |
| AE-005 | Component | Backend API Routes | CAP-001 through CAP-006 | Internal architecture constraint | ADR-002 |
| AE-006 | Component | Task Application Service | CAP-001 through CAP-006 | Internal architecture constraint | ADR-002 |
| AE-007 | Boundary | Board Repository Port | CAP-005 | Internal architecture constraint | ADR-002 |
| AE-008 | Component | SQLite Persistence Adapter | CAP-005 | Confirmed architect decision | ADR-002 |
| AE-009 | Component | Status Counter | CAP-006 | Internal architecture constraint | None |
| AE-010 | Deployment node | Local Application Runtime | CAP-001 through CAP-006 | Confirmed architect decision | ADR-003 |

## Requirements-to-Architecture Coverage

| Capability | Stories | Architecture elements | Coverage | Evidence |
|---|---|---|---|---|
| CAP-001 | US-0001 | Browser Frontend; Flask Backend; Backend API Routes; Task Application Service; SQLite Persistence Adapter | Covered | Sections 5, 6, and 8 |
| CAP-002 | US-0002 | Browser Frontend; Flask Backend; Backend API Routes; Task Application Service; SQLite Persistence Adapter | Covered | Sections 5, 6, and 8 |
| CAP-003 | US-0003 | Browser Frontend; Flask Backend; Backend API Routes; Task Application Service; SQLite Persistence Adapter | Covered | Sections 5, 6, and 8 |
| CAP-004 | US-0004 | Browser Frontend; Flask Backend; Backend API Routes; Task Application Service; SQLite Persistence Adapter | Covered | Sections 5, 6, and 8 |
| CAP-005 | US-0005 | Browser Frontend; Flask Backend; Board Repository Port; SQLite Persistence Adapter; Persistence Mechanism | Covered | Sections 5, 6, 8, and 11 |
| CAP-006 | US-0006 | Browser Frontend; Flask Backend; Status Counter | Covered | Sections 5, 6, and 8 |

## Architecture Validation

- **arc42 structure validator:** Passed
- **Container structure validator:** Passed
- **Structurizr model validator:** Passed
- **Diagram documentation validator:** Passed
- **Docker Compose validator:** Passed
- **Architecture hygiene validator:** Passed
- **Product behavior discipline validator:** Passed
- **Architecture package validator command:** `python3 .agents/skills/d-design-product-architecture/scripts/validate_architecture_package.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md sdlc_docs/02_architecture --require-report-sync`
- **Validation report synchronized:** Yes
- **Unresolved material decisions:** 0
- **Unsupported product behavior introduced:** 0
- **Validation result:** Passed

## Approval Record

| Architecture baseline | Decision | Reviewed by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
| ARCH-0002 | Approved | Edwin Carreno | SSC Developer | 2026-07-27 | None |
