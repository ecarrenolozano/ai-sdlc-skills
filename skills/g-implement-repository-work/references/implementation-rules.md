# Implementation Rules

## Scope

Implement one explicitly selected issue. Keep the diff limited to that issue and directly required tests or documentation.

## Code design

Create or update developer-owned code-level design before local writes. The design may define modules, classes, functions, route handlers, interactions, and internal schemas inside approved architecture boundaries. Update the central `sdlc_docs/02_architecture/code-level.md` index and relevant `sdlc_docs/02_architecture/containers/<container>/code-level.md` maps when meaningful code structure or contracts are introduced or changed. Use Mermaid diagrams when they clarify non-trivial sequence, flow, class/module, or object/state design.

Route material architecture, dependency, persistence, deployment, or product-behavior decisions backward instead of hiding them in implementation.

## Best practices

Read `references/best-practices/README.md` and only the linked markdown files relevant to the selected issue. If no relevant reference exists, state that in the proposal and use repository conventions.

## Ping-Pong TDD

Use `Tester driver` and `Developer navigator` roles before the proposal. When subagents are available, run both roles simultaneously and ensure their names contain those exact words; otherwise simulate both named roles explicitly in the proposal.

Treat Ping-Pong TDD as an ordered cycle during implementation: `Tester driver` proposes or creates the test that defines intended logic, the main agent confirms meaningful RED, and only then `Developer navigator` proposes or creates the minimum production code needed to pass that test. Do not let Developer navigator add production behavior before RED.

Keep the user informed as the cycle runs: report what each role is doing, which tests are proposed, which tests are created, and the current RED, GREEN, or REFACTOR status after each implementation step.

## Handoffs

- Route unclear behavior to `c-manage-product-requirements`.
- Route material architecture impact to `d-design-product-architecture`.
- Route issue drift to `e-sync-repository-requirements`.
- Route repository-wide tooling or foundation gaps to `f-establish-technical-foundation`.

## Local changes

Require approval of the visible proposal before modifying files. Re-read affected files immediately before writing.

## Local status tracking

After local tests, quality commands, and the result validator pass, update local implementation status-tracking documentation. Always consider `sdlc_docs/trace_workflow.md`, `sdlc_docs/03_implementation/backlog_priority.md`, and any existing local implementation tracker that records issue completion, remaining work, current status, or next action.

Keep the Implementation row `In Progress` until all approved initial-release implementation issues are complete and validated. Mark it `Complete` only when no planned implementation issues remain.

In backlog priority docs, keep priority rationale intact but mark completed local implementation issues and refresh the next recommended issue when the selected issue is finished. Do not mutate GitHub issues or project boards.

Do not edit requirements, architecture, repository preparation, technical foundation, or synchronization rows unless the user separately approves that governance change.

## Deviations

Request new approval for a new dependency, broader scope, architecture change, issue split, or repository-wide foundation change.

## Remote actions

Do not commit, push, open a pull request, comment on an issue, alter labels, move board state, or close work without separate approval.

## Durable records

Keep durable behavior in tests and code. Update code-level architecture docs and local status-tracking docs when implementation changes meaningful structure, contracts, issue status, remaining work, or next action. Do not create TDD log files.
