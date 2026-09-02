# Browser Task Board Workflow Orchestration Golden Example

This progressive example shows how `sdlc-orchestrate-workflow` reads workflow trace snapshots, recommends the next skill, and proposes trace repairs without performing another skill's work.

The example is a laboratory artifact. It demonstrates orchestration behavior without making Browser Task Board facts part of the general skill.

## Files

- `workflow-snapshot-early.md`: early workflow state and recommendation.
- `workflow-snapshot-after-foundation.md`: foundation complete and implementation ready.
- `workflow-snapshot-after-implementation.md`: implementation evidence exists and BDD validation should run.
- `workflow-snapshot-missing-validation-row.md`: trace is missing the new validation row.
- `recommendation-examples.md`: concise outputs for common prompts.
- `trace-repair-proposal.md`: approved-change proposal format for adding missing rows.
- `blocked-gate-examples.md`: examples of blocker reporting.
