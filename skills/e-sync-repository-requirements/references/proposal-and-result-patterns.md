# Proposal and Result Patterns

Keep proposals concise enough for a human to approve safely. Do not save them as files.

## Proposal for approved stories

```markdown
I inspected the approved requirements and the current GitHub state.

### Repositories identified

| Repository | Relationship | Verified role | Proposed access |
|---|---|---|---|
| organization/task-board | Primary repository | Main tracker and project | Write target |
| contributor/task-board | Fork | Branch and pull-request source | Read-only context |

### Current coverage

- US-0001 is covered by #12.
- US-0002 is jointly covered by #14 and #16.
- US-0003 has no verified remote work after searching open and closed issues.

### Proposed changes

1. Add the managed approved-scope section to #12.
2. Create one issue for US-0003.

New issue justification: US-0003 contains concrete approved work that is not represented by any existing issue and cannot be added coherently to another open issue.

### Destination

- Repository: organization/task-board
- GitHub Project: Task Board Development
- Column: Product Backlog
- Known automation: moving to Product Backlog does not start implementation; no additional workflow was identified.

### Not included

- No labels, assignments, milestones, comments, closures, or subissue changes.
- No other repositories will be modified.

Approve all changes, approve selected numbered actions, or reject the proposal.
```

## Proposal for a Triage issue

```markdown
Issue #27 proposes CSV export, which is not present in the approved requirements.

Recommendation: use the same issue as the source for c-manage-product-requirements.

No issue content, project placement, labels, comments, or requirements will be changed in this step.
```

## Multiple possible matches

```markdown
US-0003 has two plausible matches:

| Issue | Coverage | Important difference |
|---|---|---|
| #18 | Complete | Contains implementation discussion and linked pull request |
| #27 | Partial | Covers description editing only |

Recommendation: reuse #18 for the approved story and retain #27 as related work. No issue will be closed or changed without approval.
```

When several issues jointly cover a story, show criterion-level coverage rather than forcing one issue to be selected.

## Insufficient context

```markdown
I could read the approved stories, but I could not verify the repository's current issues, project destination, and automation effects.

No issue will be created or modified because duplicates and operational consequences cannot be ruled out.

Missing context:
- GitHub Project visibility
- open and closed issue search
- project automation rules
```

## Execution result

```markdown
Execution result:

- Action 1 completed: #12 now contains the approved managed section; read-back verified.
- Action 2 completed: #34 created and added to Product Backlog; read-back verified.
- Action 3 stopped: a new possible duplicate #35 appeared before creation.

No completed action was rolled back. No replacement issue was created. A new decision is required only for Action 3.
```

## Partial approval

Interpret natural responses narrowly:

- "Create the two new issues, but do not place them on the board" authorizes creation only when the proposal already showed creation without placement as a safe outcome.
- "Link the existing issues only" authorizes only the listed managed-section or reference updates.
- "Do everything" applies only to the latest visible proposal, not to hidden or newly discovered actions.
