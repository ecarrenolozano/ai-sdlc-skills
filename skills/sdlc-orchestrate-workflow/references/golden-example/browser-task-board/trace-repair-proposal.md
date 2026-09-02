# Trace Repair Proposal

## Problem

`trace_workflow.md` has a Pull request row but no User story validation row, and the implementation handoff points directly to `h-create-implementation-pull-request`.

## Proposed Changes

Add:

```markdown
| User story validation | Initial Release | Not Started | BDD User Story Completion Validation | implemented US-0001 available | BDD validation has not run | Run i-validate-user-story-completion |
```

Change only the `Implementation` row `Next action`:

```text
Run h-create-implementation-pull-request
```

to:

```text
Run i-validate-user-story-completion for US-0001
```

## Not Included

- No row is marked complete.
- No approval data is invented.
- No BDD scenarios are created.
- No pull request or remote action is performed.
