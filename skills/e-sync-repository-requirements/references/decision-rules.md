# Decision Rules

Use this reference to choose the least disruptive action.

## Coverage decisions

### No matching issue

Propose a new issue only after verifying open and closed issues, related repositories, templates, project destination, and automation effects. State the exact missing approved work and why no existing issue can represent it.

### One issue fully covers a story

Reuse the issue. Add or update the managed approved-scope section only when the relationship is not already clear and the edit is useful.

### Several issues jointly cover a story

Recognize the joint coverage. Do not create a story-level coordinator by default. Explain which approved criterion each issue covers and identify gaps, overlaps, or contradictions.

### One issue covers several stories

Reuse the issue when its scope is coherent. Add multiple stable story references only when useful. Do not split merely to force one issue per story.

### Partial coverage

Prefer extending a suitable open issue when the addition remains coherent. Otherwise propose only the concrete uncovered work. Do not recreate the entire story.

### Overlap without duplication

Keep both issues when they own independently useful work. Clarify overlapping criteria in the analysis. Do not close or merge either issue.

### Conflicting issues

Stop and request a product decision. Recommend `c-manage-product-requirements` when the approved behavior does not resolve the conflict.

### Approved plus unapproved behavior in one issue

Do not treat the entire issue as approved. Explain the boundary. Recommend separating or clarifying only when it reduces ambiguity, and require approval before any edit or new issue.

### Closed issue

Use it for history and duplicate prevention. Determine which requirement version it covered. Do not reopen it and do not claim validation from closure.

## Triage routing

### New product behavior

Recommend `c-manage-product-requirements` with the same source issue. Leave the issue unchanged until the product decision is approved.

### Change to approved behavior

Recommend `c-manage-product-requirements`. After approval, reconcile the same issue or affected existing issues.

### Bug

Link conceptually to the violated approved behavior. Use a natural bug format. Do not invent a user story.

### Technical improvement

Use the smallest tracking surface that remains understandable. If the technical work is repository foundation setup and Technical foundation is not `Complete`, recommend `f-establish-technical-foundation`. Route to the technical backlog only when the work is independently reviewable, too large or risky for foundation work, blocks multiple stories in a way that needs separate ownership, or cannot be represented clearly inside the dedicated foundation workflow or an existing approved issue after foundation completion. Reference architecture only when it adds practical context. Do not invent product value or user-story wording.

### Architecture-derived foundation work

Do not create one issue per architecture element, folder, dependency, or configuration file by default. Prefer:

1. `f-establish-technical-foundation` when Technical foundation is not `Complete`;
2. existing approved issue after foundation completion;
3. one coherent technical issue only when separate review/ownership is truly useful.

### Duplicate candidate

Show the candidates, coverage comparison, active discussion, linked work, and repository roles. Recommend but never close, merge, or delete.

### Question or support

Recommend a human response. Do not force it into requirements or implementation work.

### Out of scope

Explain the mismatch. Leave retain, defer, or close decisions to a person.

### Insufficient information

Recommend one precise clarification. Do not create speculative work.

## Repository and fork decisions

### Fork used for contributions

Use the upstream tracker when product governance and project planning live upstream. Use the fork for code branches and pull requests only.

### Independent fork

Use the fork tracker when the fork has its own product scope, issues, project, releases, and maintained divergence.

### Both trackers intentionally active

Create work in both only when the issues represent different operational responsibilities. State the distinct purpose of each.

### Ambiguous tracker

List all repositories and evidence. Perform no remote write until a person confirms the target.

## Creation-minimization test

Before proposing any issue, answer all of these:

1. Is there concrete approved work not represented remotely?
2. Were open and closed issues searched?
3. Were explicitly related repositories searched?
4. Can an existing issue or set of issues represent the work?
5. Can a minimal update to an open issue represent the missing scope coherently?
6. Is the target repository verified?
7. Is the project destination verified?
8. Are known automation effects visible?
9. Is the new issue independently useful rather than administrative noise?

Do not propose creation when any required answer is unknown.
