# Manual Priority Guidance Example

Target artifact: `sdlc_docs/03_implementation/backlog_priority.md`

## Source

- Repository issue source inspected: open unresolved issues for Browser Task Board.
- Remote actions: None performed.
- Purpose: help humans manually organize the product backlog before selecting one issue for implementation.

## Suggested Order

1. `US-0001 - Create a task`
   - Establishes the core task model, create API behavior, and first board response.
2. `US-0005 - Restore saved board state`
   - Stabilizes persistence expectations before later operations depend on saved board state.
3. `US-0006 - View task-status counts`
   - Stabilizes the board response shape used by multiple interactions.
4. `US-0002 - Move a task between board sections`
   - Depends on existing tasks and benefits from stable counts.
5. `US-0003 - Edit a task`
   - Depends on task identity and core update behavior.
6. `US-0004 - Delete a task`
   - Completes CRUD behavior after creation, persistence, counts, movement, and edits are understood.

## Notes

- This is manual planning guidance only.
- No GitHub issue, GitHub Project, product requirement, architecture, source code, or test file is changed by this planning result.
