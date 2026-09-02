---
name: a-clarify-project-request
description: Analyze one or more informal sources for a new software project and create, update, or review a concise Clarified Project Request. Use when emails, meeting notes, transcripts, documents, or self-authored ideas are stored in or provided for `sdlc_docs/00_inception/sources/` and are not yet clear enough to form a Project Context. Preserve original evidence, explain the inception structure, identify no more than 20 project-level uncertainties, record stakeholder answers and impacts, detect contradictions, manage document state, and prepare the result for human readiness approval. Do not generate Project Context, detailed requirements, user stories, architecture, implementation plans, or approval decisions.
---

# Project Request Clarification

## Purpose

Transform one or more informal software-project sources into a concise, traceable, and human-approved input for the downstream `b-form-project-context` skill, which performs Project Context Formation.

Act as a requirements analyst and inception facilitator. Create, update, and review the Clarified Project Request, but never act as its approver.

## Inception Structure and Artifact Purposes

Use this structure:

```text
sdlc_docs/
└── 00_inception/
    ├── README.md
    ├── sources/
    │   ├── README.md
    │   └── <original source files>
    ├── clarified_project_request.md
    └── project_context.md
```

Explain the purpose of each location whenever creating, reviewing, or presenting it. Do not assume that a person or AI understands intent from filenames alone.

### `sdlc_docs/00_inception/`

Store artifacts used to understand and establish a new software project before detailed requirements, architecture, or implementation planning begin.

Do not store detailed requirements, user stories, architecture decisions, implementation plans, or test plans here.

### `sdlc_docs/00_inception/README.md`

Explain the inception stage and the relationship between its contents. This file is expected to be created by the project template. When missing, report the structural inconsistency. Restore it from `references/inception-readme-template.md` only with explicit user authorization.

### `sdlc_docs/00_inception/sources/`

Preserve original, unrefined evidence such as informal requests, emails, meeting notes, transcripts, existing-system notes, and stakeholder documents.

Never rewrite, summarize in place, normalize, or replace an original source. Preserve later evidence as a new file.

### `sdlc_docs/00_inception/sources/README.md`

Explain that the directory contains source evidence. This file is expected to be created by the project template. When missing, report the structural inconsistency. Restore it from `references/sources-readme-template.md` only with explicit user authorization.

### `clarified_project_request.md`

Store the clarified interpretation of the original request, project-level questions, stakeholder answers, answer impacts, contradictions, and readiness approval.

Answer: **Is the original request clear enough to form a Project Context?**

Do not define detailed requirements, user stories, architecture, implementation tasks, or test cases.

### `project_context.md`

Reserve for the downstream skill. Store the approved general foundation for the project and first release: purpose, users, broad boundary, constraints, risks, responsibilities, and success conditions.

Answer: **What general context should guide the first release?**

### Artifact Relationship

```text
Original sources
    ↓
clarified_project_request.md
    ↓
project_context.md
    ↓
product_requirements.md
```

Do not treat these artifacts as interchangeable or copy one artifact wholesale into the next.

## Operating Modes

Select the mode from the request and available files.

### Draft

Use when sources exist and `sdlc_docs/00_inception/clarified_project_request.md` does not.

- Verify the inception directories and explanatory READMEs.
- Report missing structural files instead of creating them silently.
- Restore missing READMEs from the bundled templates only with explicit user authorization.
- Preserve every original source under `sources/` or record an explicit external source reference.
- Create the output from `references/clarified-project-request-template.md`.
- Set `Document state` to `Draft`, then `Under Clarification` after questions are created.
- Record source metadata.
- Draft the `Initial Understanding`.
- Create only necessary project-level questions.
- Leave unanswered questions `Open`.
- Leave readiness approval unapproved.

### Update

Use when the output exists and new answers or sources are provided.

- Update the existing document; never replace it with a blank template.
- Preserve each new source under `sources/`.
- Record each answer below its question, who answered, and the impact.
- Synchronize the `Initial Understanding` after meaningful clarification.
- Keep blocking questions `Open`.
- Detect contradictions rather than resolving them silently.

### Review

Use when preparing for human approval.

- Verify every material claim is supported by a source or recorded answer.
- Verify referenced source files exist or external references are explicit.
- Verify answered questions include impacts.
- Identify contradictions, unsupported claims, stale summary content, and premature technical detail.
- Remove unused placeholders.
- Set `Document state` to `Pending Approval` only when no blocking uncertainty remains.
- Never select `Ready` or `Not Ready`, or invent approver data.

## Required Inputs

Use the available combination of:

- Original files under `sdlc_docs/00_inception/sources/`.
- `sdlc_docs/00_inception/clarified_project_request.md` when updating or reviewing.
- New stakeholder answers, emails, notes, transcripts, corrections, or external source references.

Preserve each original source independently. Never modify a file under `sources/`.

## Workflow

1. Verify that `sdlc_docs/00_inception/` exists.
2. Verify that `sdlc_docs/00_inception/sources/` exists.
3. Verify that these structural documentation files exist:
   - `sdlc_docs/00_inception/README.md`
   - `sdlc_docs/00_inception/sources/README.md`
4. Verify that `sdlc_docs/trace_workflow.md` exists.
5. If `sdlc_docs/trace_workflow.md` is missing:
   - Report the structural inconsistency.
   - Stop the workflow.
   - Do not create, reconstruct, or restore the file.
   - Explain that the project template must provide this structural artifact.
6. If an inception directory or structural README is missing:
   - Report the inconsistency.
   - Do not create or overwrite it silently.
   - Offer to create a missing inception directory or restore a missing README from its bundled template when available.
   - Perform the repair only with explicit user authorization.
7. Explain the purpose of:
   - `sources/`
   - `clarified_project_request.md`
   - `project_context.md`
   - `trace_workflow.md`
8. Receive one or more informal project sources.
9. Discover the relevant source files under `sdlc_docs/00_inception/sources/`.
10. Do not depend on a specific source filename.
11. Preserve each source under `sources/`, or record an explicit external source reference when local preservation is not possible.
12. Never overwrite, rewrite, normalize, or summarize a preserved source in place.
13. Update the `Project request` row in `sdlc_docs/trace_workflow.md` when clarification begins:
    - Set `Status` to `In Progress`.
    - Set `Current activity` to `Request Clarification`.
    - Record the discovered source files in `Evidence`.
    - Record the current uncertainty in `Missing or blocked`.
    - Set `Next action` to `Continue a-clarify-project-request`.
14. Check whether `sdlc_docs/00_inception/clarified_project_request.md` already exists.
15. If the document does not exist:
    - Create it from `references/clarified-project-request-template.md`.
    - Set `Document state` to `Draft`.
16. If the document already exists:
    - Load it.
    - Continue from its current state.
    - Never replace it with a blank template.
17. Read and analyze all relevant sources.
18. Record the metadata or reference for every source used.
19. Draft or update the `Initial Understanding`.
20. Identify uncertainties that could materially change the Project Context.
21. Create or update no more than 20 project-level critical questions.
22. Ask fewer questions when the available information is already sufficient.
23. Present questions in small clarification rounds rather than asking all questions at once.
24. Set `Document state` to `Under Clarification` while unanswered questions or blocking uncertainty remain.
25. Update the `Project request` row while clarification is active:
    - Keep `Status` as `In Progress`.
    - Keep `Current activity` as `Request Clarification`.
    - Record `00_inception/clarified_project_request.md` and relevant source files in `Evidence`.
    - Summarize the blocking uncertainty in `Missing or blocked`.
    - Set `Next action` to `Continue a-clarify-project-request`.
26. If answers are unavailable:
    - Present only the next necessary clarification questions.
    - Wait for stakeholder clarification.
    - Recheck whether answers are available before continuing.
27. When answers are provided:
    - Record each answer directly below its matching question.
    - Record who answered.
    - Describe what the answer confirms, changes, or excludes in the `Impact` field.
28. If new documentary evidence arrives, preserve it as a new source file.
29. If an answer is provided directly through chat and no independent source file exists, record it in the Clarified Project Request.
30. Update the `Initial Understanding` using confirmed clarifications.
31. Check the document for:
    - Contradictions.
    - Unsupported claims.
    - Stale summary content.
    - Premature technical detail.
32. If blocking uncertainty remains:
    - Keep `Document state` as `Under Clarification`.
    - Keep unresolved questions marked `Open`.
    - Request only the additional clarification needed.
    - Update the `Project request` row with the current blocking uncertainty.
    - Return to uncertainty identification and continue the clarification loop.
33. When no blocking uncertainty remains, set `Document state` to `Pending Approval`.
34. Update the `Project request` row when approval is pending:
    - Keep `Status` as `In Progress`.
    - Keep `Current activity` as `Request Clarification`.
    - Record `00_inception/clarified_project_request.md` in `Evidence`.
    - Set `Missing or blocked` to `Human readiness approval pending`.
    - Set `Next action` to `Obtain human approval`.
35. Submit the document to the authorized human approver.
36. Require the authorized approver to record:
    - `Ready` or `Not Ready`.
    - Their name.
    - Their role.
    - The approval date.
    - Any blocking issues.
37. Do not select `Ready` or `Not Ready` on behalf of the approver.
38. Do not invent the approver's name, role, date, or blocking issues.
39. If the approval decision or required approver fields are incomplete, request the missing information and keep `Document state` as `Pending Approval`.
40. If `Ready` is selected while blocking issues are recorded, report the contradiction and request a corrected approval decision. Keep `Document state` as `Pending Approval`.
41. After a complete and internally consistent human decision is recorded, set `Document state` to `Closed`.
42. If the approver selects `Ready` and `Blocking Issues` is `None`, update the `Project request` row:
    - Set `Status` to `Complete`.
    - Set `Current activity` to `Request Clarification`.
    - Record `00_inception/clarified_project_request.md` in `Evidence`.
    - Set `Missing or blocked` to `None`.
    - Set `Next action` to `Run b-form-project-context`.
43. After a valid `Ready` approval, update the `Project context` row:
    - Keep `Status` as `Not Started`.
    - Set `Current activity` to `Project Context Formation`.
    - Record the approved `00_inception/clarified_project_request.md` in `Evidence`.
    - Set `Missing or blocked` to `Project Context not created`.
    - Set `Next action` to `Run b-form-project-context`.
44. Pass the approved Clarified Project Request to `b-form-project-context` only after a valid `Ready` approval.
45. Identify Project Context Formation as the next stage.
46. If the approver selects `Not Ready`:
    - Keep `Document state` as `Closed`.
    - Do not pass the document downstream.
47. After a `Not Ready` decision, update the `Project request` row:
    - Set `Status` to `Blocked`.
    - Set `Current activity` to `Request Clarification`.
    - Record `00_inception/clarified_project_request.md` in `Evidence`.
    - Copy the documented approval blocking issues into `Missing or blocked`.
    - Set `Next action` to `Resolve blocking issues with a-clarify-project-request`.
48. Preserve all unrelated rows and active increment records in `sdlc_docs/trace_workflow.md`.
49. Do not replace the complete traceability table when only rows owned or directly affected by `a-clarify-project-request` require modification.
50. `a-clarify-project-request` owns the `Project request` row and may update the `Project context` row only to expose the approved handoff to `b-form-project-context`.

Read `references/process-flowchart.md` when explaining or verifying this workflow.

The written workflow and flowchart must represent the same:

- Structural checks and repair boundaries.
- Source discovery and preservation.
- Clarification loop and evidence handling.
- Maximum question limit and small clarification rounds.
- Workflow traceability updates.
- Human approval completion and contradiction handling.
- `Ready` and `Not Ready` outcomes.
- Handoff to `b-form-project-context`.

## Source Preservation Rules

- Treat `sources/` as evidence, not working documentation.
- Use meaningful filenames.
- Keep generated artifacts outside `sources/`.
- Preserve later clarifications as new files when they arrive as documents, notes, emails, or transcripts.
- Record direct chat answers in the Clarified Project Request when no independent source exists.
- Reference source filenames without copying complete source contents.
- Keep external links when local preservation is impossible.
- This folder is not a general-purpose file repository. Do not store unrelated files here or heavy ones such as images, videos, or large datasets. Use a separate repository for those.

## Document State Rules

- `Draft`: created but not completely analyzed.
- `Under Clarification`: questions are open or answers are being incorporated.
- `Pending Approval`: no blocking uncertainty remains and a formal decision is pending.
- `Closed`: an authorized approver selected `Ready` or `Not Ready`.

Only the `Readiness Approval` section determines whether the project may advance.

## Critical Question Rules

- Ask no more than 20 questions.
- Ask fewer when sufficient.
- Ask only questions whose answers could materially change the Project Context.
- Keep questions at project level.
- Prioritize problem, outcome, users, rationale, broad initial boundary, constraints, deadlines, success, ownership, dependencies, and material risks.
- Do not repeat answered information.
- Defer detailed functional questions to requirements clarification.
- Defer technical questions to architecture and implementation planning.
- Treat named technologies as proposals unless explicitly mandatory.

Do not ask about frameworks, libraries, programming languages, components, schemas, storage, APIs, field validation, algorithms, tests, repository structure, or deployment configuration unless explicitly mandatory at project level.

## Evidence and Uncertainty Rules

Distinguish internally between supported information, interpretation, proposed solution, assumption, open uncertainty, and contradiction.

Never invent answers or silently promote interpretations to confirmed facts. Keep source conflicts visible and ask for resolution when material.

## Output Rules

Write the generated artifact to:

```text
sdlc_docs/00_inception/clarified_project_request.md
```

Use `references/clarified-project-request-template.md` unless a compatible variation is explicitly requested.

Keep the document concise:

- Maintain one current `Initial Understanding`.
- Use no more than 20 critical questions.
- Keep answers and impacts brief.
- Remove unused question blocks before approval review.
- Store answers directly below questions.
- Do not create a separate clarification log.
- Reference sources without duplicating them.

When presenting an artifact, state:

- Its path.
- Its purpose.
- Whether it is source evidence, generated interpretation, or approved downstream content.
- Which exact skill identifier consumes it next and the human-readable stage that skill performs.

Never:

- Modify a source file.
- Store generated inception artifacts in `sources/`.
- Approve on behalf of a human.
- Invent approver identity, role, or date.
- Close the document before a human decision is recorded.
- Generate Project Context in the same operation unless separately invoked after approval.

## Workflow Traceability

Maintain the central workflow status in:

```text
sdlc_docs/trace_workflow.md
```

`a-clarify-project-request` owns the `Project request` row.

When `a-clarify-project-request` starts:

- Set `Status` to `In Progress`.
- Set `Current activity` to `Request Clarification`.
- Reference the available source evidence.
- Record any missing information or blocking uncertainty.
- Set `Next action` to `Continue a-clarify-project-request`.

When the Clarified Project Request reaches `Pending Approval`:

- Keep `Status` as `In Progress`.
- Record `clarified_project_request.md` as evidence.
- Record that human readiness approval is pending.
- Set `Next action` to `Obtain human approval`.

When the document is closed with a valid `Ready` decision:

- Set `Status` to `Complete`.
- Set `Current activity` to `Request Clarification`.
- Record `00_inception/clarified_project_request.md` as evidence.
- Set `Missing or blocked` to `None`.
- Set `Next action` to `Run b-form-project-context`.

Also update the `Project context` row to show that the approved Clarified Project Request is available and that `b-form-project-context` may begin Project Context Formation.

When the document is closed with `Not Ready` selected:

- Set `Status` to `Blocked`.
- Record the Clarified Project Request as evidence.
- Copy the documented blocking issues into `Missing or blocked`.
- Set `Next action` to `Resolve blocking issues with a-clarify-project-request`.

Do not replace the entire traceability table. Update only the rows owned or directly affected by `a-clarify-project-request`.

Preserve all unrelated rows and active increment records.

## Golden Example

Use the shared TODO-board project as the canonical example.

Store the example separately:

```text
references/
└── golden-example/
    ├── in-informal-project-request.md
    └── out-clarified-project-request.md
```

The transformation is:

```text
references/golden-example/in-informal-project-request.md
    ↓
references/golden-example/out-clarified-project-request.md
```

Equivalent real project paths are:

```text
sdlc_docs/00_inception/sources/informal_project_request.md
    ↓
sdlc_docs/00_inception/clarified_project_request.md
```

The Golden Example may contain fictional answers and approval data only to demonstrate a complete result. Never invent these during real execution or copy project-specific facts into unrelated work.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
