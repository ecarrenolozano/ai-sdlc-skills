# Completion Gates

## Backlog Priority Planning

Before reporting backlog priority planning ready for review, confirm:

- unresolved issues or approved work items were inspected;
- ranking criteria from `references/backlog-priority-policy.md` were applied;
- `sdlc_docs/03_implementation/README.md` exists or was updated;
- `sdlc_docs/03_implementation/backlog_priority.md` exists or was updated;
- the priority order is presented as manual guidance, not an automatic selection or estimate;
- no production code, test code, requirements, architecture, ADR, dependency, foundation, GitHub issue, or GitHub Project mutation occurred unless separately approved.

## Single Issue Implementation

Before reporting local implementation ready for review, confirm:

- one selected issue remained in scope;
- approved acceptance criteria or defect behavior are covered;
- code-level design stayed aligned with approved architecture;
- `sdlc_docs/02_architecture/code-level.md` exists, was updated, or was explicitly justified as already current;
- relevant `sdlc_docs/02_architecture/containers/<container>/code-level.md` maps exist, were updated, or were explicitly justified as already current;
- Mermaid diagrams were included for non-trivial sequence, flow, class/module, or object/state design, or omitted with a clear reason;
- relevant best-practice references were applied or declared unavailable/not applicable;
- Ping-Pong TDD `Tester driver` and `Developer navigator` roles were used with subagents or explicitly simulated;
- the user was kept informed about both roles, proposed tests, created tests, and current RED-GREEN-REFACTOR status;
- meaningful RED evidence exists for new behavior or bug reproduction;
- target and related tests are green;
- refactoring preserved green results;
- repository quality commands were executed;
- local implementation status-tracking documentation was updated after validation, or each existing tracker was left unchanged with an explicit reason that it was already current;
- `sdlc_docs/trace_workflow.md` records implementation traceability in the Implementation row or implementation-owned fields;
- `sdlc_docs/03_implementation/backlog_priority.md`, when present, marks completed local implementation issues and refreshes remaining work or next recommended issue;
- the Implementation row status remains `In Progress` when approved implementation issues remain, and becomes `Complete` only when no planned implementation issues remain;
- local status tracking records the selected issue, test and quality evidence, code-level docs, remaining gaps, and next action;
- no tests were weakened, skipped, or removed to obtain success;
- no unrelated product behavior was added;
- no unapproved dependency, architecture, or foundation change occurred;
- the final diff is explainable by the issue;
- no commit, push, pull request, issue transition, or closure occurred without separate approval.

Report failures and environment limitations rather than hiding them.
