# Issue Content Patterns

Use the repository's compatible issue template when available. These patterns are fallbacks and examples, not a second mandatory template system.

## New issue for one approved story

Title:

```text
US-0003 - Edit an existing task
```

Body:

```markdown
## User story

As a task-board user,
I want to edit an existing task,
so that I can correct or update its information.

## Acceptance criteria

**Scenario: Edit an existing task**

Given an existing task
When I edit its content
Then the updated content is displayed

## Project references

- User story: US-0003
- Requirement: REQ-0001
- Capability: CAP-003

<!-- sdlc-user-story: US-0003 -->
```

Reuse approved text exactly. Include only references that are stable and useful.

## Issue for a concrete missing part

Use this only when existing issues cover the rest of the story and the missing part is an independently useful unit of work.

```markdown
## Scope

Preserve edited task content during the browser session.

## Acceptance criteria

Given an edited task
When the board is refreshed during the same browser session
Then the edited content remains available

## Project references

- User story: US-0003
- Coverage: Session persistence after editing
```

Do not derive new criteria. Use only approved criteria or an approved subset.

## Existing human-authored issue

Preserve all existing content. Append one managed section:

```markdown
<!-- approved-scope:start -->

## Approved scope

As a task-board user,
I want to export the current tasks as CSV,
so that I can analyze them with other tools.

## Acceptance criteria

Given a board containing tasks
When I request a CSV export
Then a CSV file containing the current tasks is produced

## Project references

- User story: US-0007
- Requirement: REQ-0002

<!-- approved-scope:end -->
```

Rules:

- Add the section once.
- Update only text between the markers.
- Show the exact replacement before approval.
- Stop when markers are duplicated, damaged, or ambiguous.
- Stop when manual edits inside the section cannot be safely reconciled.
- Never replace the original issue body.

## Bug

```markdown
## Observed behavior

Tasks disappear after refreshing the browser.

## Expected behavior

Tasks created during the browser session remain available after refresh.

## Project references

- User story: US-0005
```

Do not rewrite a bug as a user story.

## Technical improvement

```markdown
## Technical objective

Remove direct storage access from the board UI so storage behavior can be tested independently.

## Architecture references

- Component: Board State Repository
- Decision: ADR-001
```

Do not invent a product story for technical work.

## Architecture references

Include architecture references only when they help execute or route the issue. Prefer stable identifiers, names, or repository links. Do not copy architecture paragraphs.

## Comments

Do not comment by default. When a comment is necessary, present its full text in the approval proposal. Keep it human-readable and specific; do not announce internal synchronization activity.
