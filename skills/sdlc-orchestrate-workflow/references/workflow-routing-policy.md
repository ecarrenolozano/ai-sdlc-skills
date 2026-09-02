# Workflow Routing Policy

## Recommendation Priority

When several rows need attention, recommend in this order:

1. Resolve `Blocked` rows with concrete missing information.
2. Continue `Under Clarification` rows with their owning skill.
3. Obtain human approval for `Pending Approval` rows.
4. Continue `In Progress` rows with their owning skill.
5. Start the first `Not Started` row whose upstream gates are complete.

If multiple active increments exist, preserve their row boundaries and report the ambiguity instead of collapsing them into the initial-release row.

## Controlled Overlap Exception

One overlap is permitted without ambiguity handling:

- `Implementation` is `In Progress`; and
- `User story validation` is `In Progress` for implemented story subsets with explicit evidence.

Under this exception, continue routing both owning skills iteratively while keeping `Pull request` and `Release deployment` inactive until their normal gates are met.

One additional overlap is permitted without ambiguity handling:

- `Implementation` is `In Progress`; and
- `Pull request` is `In Progress` for active iterative review with explicit PR evidence.

Under this exception, keep `Release deployment` inactive and continue resolving implementation and validation gaps before completion handoff.

One additional overlap is permitted without ambiguity handling:

- `Implementation` is `In Progress`; and
- `Release deployment` is `In Progress` for approved local release-preparation or smoke-deployment evidence.

Under this exception, no publishing, tagging, or external deployment actions are allowed without separate explicit approval.

One additional overlap is permitted without ambiguity handling:

- `Implementation` is `In Progress`; and
- `Pull request` is `In Progress` for iterative review; and
- `Release deployment` is `In Progress` for approved local release-preparation or smoke-deployment evidence.

Under this exception, release preparation remains local-only and cannot perform tagging, publishing, or external deployment without separate explicit approval.

## Human Actions

Some next actions are not skills:

- obtain human approval;
- review a proposal;
- provide missing stakeholder information;
- accept or reject a completed local result.

Recommend those as human actions and do not force them into a skill identifier.

## Repairs

Trace repairs are administrative, not workflow completion. A repair can make the trace structurally accurate, but it cannot prove work happened.

Before proposing a repair, show:

- the row and field to change;
- current value;
- proposed value;
- evidence that justifies the repair;
- why the owning skill does not need to perform the change itself;
- actions explicitly not included.

Require explicit approval before writing.
