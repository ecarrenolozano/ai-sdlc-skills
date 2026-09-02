# ADR-001: Browser-Local Persistence Behind a Repository Boundary

- **Status:** Superseded
- **Date:** 2026-07-24
- **Decision owners:** Edwin Carreno, SSC Developer
- **Related capabilities:** CAP-005; supports CAP-001 through CAP-004 and CAP-006
- **Affected architecture elements:** Browser Task Board App; Board State Repository; Browser Storage Adapter
- **Current use:** Historical ARCH-0001 decision; future implementation work follows ADR-002.

## Context

The ARCH-0001 baseline addressed a single-user browser task board with a one-day delivery constraint and saved board state between browser sessions. It has since been superseded by ADR-002.

The architect selected a progressive approach: use browser-local persistence now while preserving an explicit internal boundary for future approved persistence changes.

## Decision Drivers

- Meet the approved saved-board requirement.
- Keep the initial release compatible with the one-day delivery constraint.
- Avoid adding unapproved collaboration scope.
- Prevent task workflow logic from depending directly on one storage API.

## Considered Options

| Option | Decision |
|---|---|
| Direct browser-storage calls throughout the app | Rejected because storage concerns would be scattered through workflow code. |
| A larger multi-component architecture in ARCH-0001 | Rejected at the time because it added delivery risk before the later ADR-002 direction was approved. |
| Browser-local persistence behind Board State Repository | Accepted because it meets the current requirement and isolates future storage change. |

## Decision

ARCH-0001 used browser-local persistence behind Board State Repository. Task Workflow accessed storage through that boundary, and Browser Storage Adapter implemented it.

This decision is no longer implementation guidance. ADR-002 is the accepted first-release architecture for future work.

## Consequences

### Positive

- Met the then-current persistence interpretation without additional runtime components.
- Supports the one-day delivery constraint.
- Localizes future persistence replacement behind a documented boundary.

### Negative

- Data remains tied to a browser profile and device.
- Clearing browser storage can remove saved state.
- Future collaboration requires new approved Product Requirements and architecture changes.

### Risks

- Historical implementation could have bypassed Board State Repository and coupled workflow code directly to browser storage.
- Browser storage availability and quota vary by environment.

## Validation

- Historical Structurizr Component view `BrowserTaskBoardAppComponents` showed the boundary and adapter.
- CAP-005 now maps through ADR-002 to the Board Repository Port, SQLite Persistence Adapter, and Persistence Mechanism.
- Implementation planning must follow ADR-002.

## Supersedes

None.

## Superseded By

ADR-002.
