# Browser Task Board BDD Validation Golden Example

This progressive example shows how `i-validate-user-story-completion` validates an implemented story after local implementation and before pull request creation.

The example is a laboratory artifact. It demonstrates the skill's structure and expected evidence without making Browser Task Board facts part of the general skill.

## Flow

```text
in-repository/
selected-implemented-story.md
in-trace_workflow.md
    -> proposal.md
    -> bdd-mapping.md
    -> validation-execution.md
out-repository/
out-trace_workflow.md
result.md
```

## What It Demonstrates

- one implemented story selected for validation;
- Gherkin scenario placement under `tests/validation/features/`;
- pytest-bdd step placement under `tests/validation/steps/`;
- acceptance-criterion to scenario mapping;
- validation evidence with exact commands;
- trace workflow update for `User story validation`;
- no product behavior or pull request action.
