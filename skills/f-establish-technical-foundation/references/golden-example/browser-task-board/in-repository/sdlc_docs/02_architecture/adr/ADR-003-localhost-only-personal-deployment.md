# ADR-003: Localhost-Only Personal Deployment for the First Release

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision owners:** Edwin Carreno, SSC Developer
- **Related capabilities:** CAP-001 through CAP-006
- **Affected architecture elements:** Browser Frontend; Flask Backend; Persistence Mechanism; Deployment view

## Context

The approved first release is a single-user Browser Task Board. Product Requirements do not include authentication, collaboration, shared boards, multi-user data isolation, or cross-device synchronization. The approved interpretation accepts a local Python and Flask process because the user interface is accessed through the browser, not a traditional desktop application.

ARCH-0002 separates the Browser Frontend from the Flask Backend and uses SQLite backend persistence. The remaining deployment question is whether the Flask application should run as a personal local application bound only to `127.0.0.1`, or as a hosted Flask application accessible remotely.

## Decision Drivers

- Preserve the approved single-user first-release scope.
- Avoid exposing an unauthenticated task-board API to a network.
- Keep personal SQLite data isolated to the local runtime.
- Avoid adding unapproved authentication, collaboration, operations, or hosting responsibilities.
- Serve the frontend and API from one local origin.
- Keep the first release small enough for the delivery constraint.

## Considered Options

| Option | Decision |
|---|---|
| Personal local Flask application bound only to `127.0.0.1`, with a personal SQLite database | Accepted because it matches the single-user, no-authentication first release and keeps data local to the user's machine. |
| Hosted Flask application accessible remotely | Rejected for the first release because remote access without authentication would expose task data and API operations. A hosted deployment requires a future approved security and operations decision. |

## Decision

Run the initial release as a personal local web application.

The Flask Backend must bind only to `127.0.0.1` for the first release. It must not be exposed to the local network or Internet. Flask serves both the Browser Frontend and API from the same local origin. The SQLite database is a personal local database owned by one local application instance.

Authentication is not required for this local personal instance because the backend is restricted to loopback access. If the application becomes remotely accessible later, authentication and data-isolation decisions are required before deployment.

The first release must not be deployed as a publicly reachable hosted Flask application unless a later approved product and architecture change adds the required security, data-isolation, and operational model.

## Consequences

### Positive

- Avoids exposing an unauthenticated backend to the network.
- Keeps single-user data isolated to a local SQLite database.
- Reduces deployment and operational complexity.
- Preserves the approved no-authentication and no-collaboration scope.

### Negative

- The app is available only on the local machine.
- No cross-device access is provided.
- The user/developer must understand local database location, backup, and reset behavior.
- Hosted deployment will require future architecture work.

### Risks

- Misconfiguring Flask to bind to `0.0.0.0` would expose the unauthenticated API.
- Local SQLite data may be lost if the database file is deleted or not backed up.
- Later remote hosting could be attempted without adding authentication unless this decision is visible.

## Validation

- Deployment view shows local browser and local application runtime on the user device.
- Architecture constraints prohibit local-network, Internet, and public hosted deployment for the first release.
- Flask serves the frontend and API from the same local origin.
- Operational documentation must record local database path and reset/backup guidance.

## Supersedes

None.

## Superseded By

None.
