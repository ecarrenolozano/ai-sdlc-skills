# Proposal and Result Patterns

## PR Proposal

```text
Mode
Pull request proposal

Repository
- Remote: <owner/repository>
- Current branch: <branch>
- Base branch: <base>
- Working tree: <clean/dirty with summary>

Included commits
- <sha> <subject>

Implemented issues
- <issue> <title> - <local status and remote state>

Grouping rationale
- <single story/coherent batch/maintenance/mixed>
- <why these commits belong together or should be split>

Changed-file summary
- Production code: <paths or none>
- Tests: <paths or none>
- SDLC docs: <paths or none>
- Skill/tooling: <paths or none>

Validation evidence
- <command>: <result>

Local status tracking
- `sdlc_docs/trace_workflow.md`: <status>
- `sdlc_docs/03_implementation/backlog_priority.md`: <status>

Proposed PR title
<title>

Proposed PR body
<body>

Remote safety
- Auto-close keywords: <absent/present with reason>
- Approved remote actions requested: <push branch, create PR>
- Not included: issue closure, project moves, labels, assignments, merge

Approval requested
Approve only the push and PR creation described above.
```

## PR Body

```md
## Summary

- <change>
- <change>

## Implemented Issues

- Refs #<number> - <title>

## Validation

- `<command>` - <result>

## SDLC Traceability

- Requirements: <ids>
- User stories: <ids>
- Architecture: <elements>
- Code-level docs updated: <yes/no/not applicable>
- Local status tracking updated: <yes/no/not applicable>

## Remote Actions

This PR does not close or move issues automatically.
```

## Final Result

```text
Pull request created
- URL: <url>
- Base: <base>
- Head: <branch>
- Included commits: <count/list>

Validation reported
- <command>: <result>

Remote actions performed
- Pushed branch: <yes/no>
- Created PR: <yes/no>

Remote actions not performed
- No issue closure.
- No project movement.
- No labels, assignments, merge, or branch deletion.
```
