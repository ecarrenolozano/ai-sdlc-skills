# Backlog Priority Policy

## Purpose

Create manual implementation-order guidance from unresolved repository issues without changing product requirements, architecture, GitHub issues, project boards, or production code.

## Inputs

Read the current unresolved issue list, approved Product Requirements, accepted Architecture and ADRs, Workflow Traceability, existing `sdlc_docs/03_implementation/` docs, and current repository state.

## Ranking Criteria

Rank issues by these criteria, in this order:

1. **Dependency order:** implement stories that create shared model, API, storage, or UI foundations before stories that depend on them.
2. **Readiness:** prefer issues with approved acceptance criteria, clear architecture mapping, and no unresolved routing question.
3. **Architecture foundation value:** prefer issues that stabilize cross-component contracts or core boundaries early.
4. **Risk reduction:** prefer issues that expose persistence, API, validation, or integration risks before many later stories depend on them.
5. **User-visible value:** when dependencies and risks are comparable, prefer the issue that gives the user the most coherent next workflow.

## Output Rules

Create or update:

- `sdlc_docs/03_implementation/README.md`;
- `sdlc_docs/03_implementation/backlog_priority.md`.

The priority document must include:

- issue source and inspection date;
- unresolved issue inventory;
- suggested order with issue identifiers and titles;
- short rationale for each position;
- dependency, risk, and readiness notes;
- blockers or route-back decisions;
- statement that the document is manual planning guidance only.

Do not create source code, test code, implementation reports, or code-level architecture in `03_implementation`.

## Remote Boundary

Do not assign, label, reorder, transition, close, reopen, comment on, or otherwise mutate GitHub issues or GitHub Projects unless the user gives separate explicit approval for that remote action.
