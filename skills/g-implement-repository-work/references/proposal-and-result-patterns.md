# Proposal and Result Patterns

## Backlog priority planning proposal

```text
Mode
Backlog priority planning

Repository and issue source
- <repository>
- <issue list source and date>

Unresolved issue inventory
- <issue identifier and title>

Ranking criteria
- Dependency order
- Readiness
- Architecture foundation value
- Risk reduction
- User-visible value

Proposed artifacts
- Create/update: sdlc_docs/03_implementation/README.md
- Create/update: sdlc_docs/03_implementation/backlog_priority.md

Proposed priority order
1. <issue> - <rationale>

Out of scope
- Production code changes
- Code-level architecture ownership in 03_implementation
- GitHub issue or project mutation

Approval requested
Approve only the local planning-document changes described above.
```

## Local implementation proposal

```text
Mode
Single issue implementation

Selected issue
<identifier and title>

Approved behavior
- <criterion or defect>

Baseline
- <command>: <result>

Best-practice references
- <reference file read, or unavailable/not applicable>

Ping-Pong TDD review
- Tester driver: <subagent name or simulated role; tests that define intended logic, edge cases, and RED expectations>
- Developer navigator: <subagent name or simulated role; minimal implementation strategy constrained by Tester driver tests>
- Reconciled decision: <final test/design direction>

Code-level design
- Architecture elements: <C4 containers/components/ADRs involved>
- Planned code elements: <modules/classes/functions/routes/interactions>
- Central code-level index: <create/update/unchanged with reason>
- Per-container code-level maps: <create/update/unchanged with reason>
- Mermaid diagrams: <sequenceDiagram/flowchart/classDiagram/object-state diagram, or not useful with reason>

Local status-tracking plan
- Update `sdlc_docs/trace_workflow.md` after successful validation.
- Update `sdlc_docs/03_implementation/backlog_priority.md` after successful validation when it exists.
- Update any existing local implementation tracker that records issue completion, remaining work, current status, or next action.
- Scope: Implementation row or implementation-owned fields only.
- Status rule: `In Progress` until all approved implementation issues are complete; `Complete` only when no planned issues remain.
- Evidence to record: selected issue, test/quality commands, code-level docs, remaining gaps, and next action.
- Remote status rule: do not close, move, label, assign, or comment on remote issues or project boards without separate approval.

TDD plan
1. Tester driver -> <behavior> -> <test level and path> -> expected RED
2. Developer navigator -> <minimum production response after meaningful RED>

User-visible TDD status plan
- Report proposed tests after Tester driver review.
- Report created tests and command result after each RED.
- Report implementation status after each GREEN.
- Report refactor status after each REFACTOR.

Likely files
- Create: ...
- Modify: ...

Dependencies or foundation changes
- None, or list the requested deviation.

Validation commands
- ...

Out of scope
- ...

Approval requested
Approve only the local changes described above.
```

## Final result

```text
Mode
Single issue implementation

Selected issue
<identifier and title>

TDD evidence
- <behavior>
  - Proposed test: <Tester driver proposal>
  - Created test: <path>
  - RED: <command and failure reason>
  - Developer response: <Developer navigator implementation response>
  - GREEN: <command and result>
  - REFACTOR: <change and green confirmation>

Code-design review
- Architecture alignment: <confirmed or limitation>
- Code-level documents: <central and per-container created/updated/unchanged with reason>
- Mermaid diagrams: <included or omitted with reason>
- Best-practice references: <applied or unavailable/not applicable>
- Ping-Pong TDD roles: <Tester driver and Developer navigator subagents used or roles simulated>
- User-visible status updates: <proposed tests, created tests, and RED-GREEN-REFACTOR statuses reported>

Local status tracking
- `sdlc_docs/trace_workflow.md`: <updated/unchanged with reason>
- `sdlc_docs/03_implementation/backlog_priority.md`: <updated/unchanged/not present with reason>
- Other local trackers: <updated/unchanged/not present with reason>
- Implementation status: <In Progress/Complete and why>
- Evidence recorded: <issue, commands, code-level docs>
- Remaining gaps: <issue numbers/blockers or none>
- Next action: <next recommended issue or review action>

Files changed
- ...

Validation
- <command>: <exit code and result>

Scope review
- No unrelated behavior added.
- No unapproved architecture or dependency change.

Remote actions
- None performed.

Remaining limitations
- None, or exact gaps.

Next action
- Review the local diff. Any commit, push, pull request, or issue transition requires separate approval.
```
