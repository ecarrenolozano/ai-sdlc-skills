# Pull Request Policy

## Scope

Create PRs for local implementation work that has already passed the implementation workflow. The PR is a review handoff, not a place to add product behavior.

## Grouping Rules

- Prefer one PR per coherent implementation batch.
- Use one PR per story when the story is independently reviewable and meaningful.
- Group stories only when they are tightly coupled, small, validated together, and share the same architecture slice.
- Keep skill/tooling changes separate from product implementation unless the user explicitly approves a combined maintenance PR.
- Explain the grouping rationale in the proposal.

## Required Evidence

Before proposing a PR, inspect:

- commits included in the PR;
- changed files since the base branch;
- implemented issue numbers and titles;
- local status-tracking docs showing current implementation status;
- code-level architecture docs when production code changed;
- validation commands and results.

## Remote Safety

Remote actions require explicit approval. Treat each category separately:

- pushing a branch;
- creating a PR;
- commenting on issues;
- changing issue labels, assignees, milestones, or project fields;
- closing or reopening issues;
- merging a PR;
- deleting a branch.

Avoid auto-close keywords such as `closes`, `fixes`, and `resolves` unless the user explicitly wants issue closure on merge. Use neutral references such as `Refs #1` or `Implements #1 without auto-closing`.

## Local Status Tracking

When local trackers exist, PR proposals should report whether they show:

- which issues are locally implemented;
- which issues remain;
- the next recommended issue;
- whether a PR has been created or is only proposed.

Do not rewrite local status trackers during PR creation unless the proposal includes the exact local document edits and the user approves them.
