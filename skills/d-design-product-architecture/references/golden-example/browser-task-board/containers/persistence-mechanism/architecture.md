# Persistence Mechanism Architecture

- **Structurizr container identifier:** persistenceMechanism
- **Container folder:** persistence-mechanism
- **Decision status:** Confirmed architect decision
- **Evidence basis:** CAP-005 / US-0005 requires board state restoration between browser sessions.

## Container Identity

Persistence Mechanism represents SQLite backend persistence for preserving board state in the initial release.

## Purpose

Store and restore board state for the Flask Backend using SQLite.

## Responsibilities

- Preserve board state in SQLite according to the approved persistence semantics.
- Support loading saved state when the user returns to the app.
- Remain behind the Flask Backend persistence adapter.

## Interfaces Provided

A storage interface consumed only by the Flask Backend persistence adapter.

## Interfaces Consumed

Local filesystem storage used by SQLite.

## Data Ownership

SQLite owns durable board-state storage according to the approved strategy. One local first-release application instance owns one personal SQLite database. Product behavior and validation remain owned by the Flask Backend.

## Dependencies

SQLite. Exact database path, schema, migration approach, and reset behavior remain technical-foundation decisions.

## Internal Building Blocks

No deeper architecture decomposition is required. Exact tables and schema belong to technical foundation and implementation planning.

## Runtime Responsibilities

The Flask Backend SQLite persistence adapter reads and writes board state through SQLite.

## Quality Attributes

- Must satisfy the approved restore-saved-board behavior.
- Must not introduce cross-device synchronization unless that product behavior is approved.
- Must not force frontend code to depend on storage internals.

## Constraints

- The Browser Frontend must not access this mechanism directly.
- The backend must expose persistence effects only through the approved HTTP/JSON API.
- The SQLite database is local to the personal first-release runtime.
- Do not treat the SQLite database as shared hosted storage in the first release.

## Related ADR

- [ADR-002: Separate the Browser Frontend from the Flask Backend](../../adr/ADR-002-separate-browser-frontend-from-flask-backend.md)

## Open Decisions

Exact SQLite schema, database file location, migration handling, and backup/reset guidance remain technical-foundation decisions.
