# Product Requirements

## 1. Document Control

- **Project:** Personal Task Board
- **Mode:** Initial release
- **Source project context or increment issue:** `sdlc_docs/00_inception/project_context.md`
- **Last updated:** 2026-07-22
- **Active scope state:** Approved

## 2. Requirements Overview

| Requirement | Requirement status | Stories | Story status | Source | Repository issues |
|---|---|---|---|---|---|
| REQ-0001 Manage task information | Approved | US-0001, US-0002, US-0003 | Approved | Approved Project Context and recorded clarifications | Not created |
| REQ-0002 Organize tasks by status | Approved | US-0004 | Approved | Approved Project Context and recorded clarifications | Not created |
| REQ-0003 View task-status counts | Approved | US-0005 | Approved | Approved Project Context and recorded clarifications | Not created |
| REQ-0004 Preserve the board | Approved | US-0006 | Approved | Approved Project Context and recorded clarifications | Not created |

### Source Statement Coverage Register

| Source ID | Source scope statement | Source location | Statement role | Decomposed into CAP IDs | Rationale |
|---|---|---|---|---|---|
| SRC-001 | Create tasks. | Included High-Level Capabilities; Success Criteria | Atomic | CAP-001 | Single independently observable source statement |
| SRC-002 | Edit existing tasks. | Included High-Level Capabilities; Success Criteria | Atomic | CAP-002 | Single independently observable source statement |
| SRC-003 | Delete tasks so they no longer appear on the board. | Included High-Level Capabilities; Success Criteria | Atomic | CAP-003 | Single independently observable source statement |
| SRC-004 | Move tasks between TODO, DOING, and DONE. | Included High-Level Capabilities; Success Criteria | Atomic | CAP-004 | Single independently observable source statement |
| SRC-005 | Display basic counts for pending, current, and completed tasks. | Included High-Level Capabilities; Success Criteria | Atomic | CAP-005 | Single independently observable source statement |
| SRC-006 | Preserve tasks and board state between browser sessions. | Included High-Level Capabilities; Success Criteria | Atomic | CAP-006 | Single independently observable source statement |

### Source Scope Coverage Matrix

| Scope ID | Atomic capability | Source IDs | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|---|
| CAP-001 | Create a task | SRC-001 | Create tasks. | Included High-Level Capabilities; Success Criteria | Covered | REQ-0001 / US-0001 | Single independently observable outcome |
| CAP-002 | Edit an existing task | SRC-002 | Edit existing tasks. | Included High-Level Capabilities; Success Criteria | Covered | REQ-0001 / US-0002 | Single independently observable outcome |
| CAP-003 | Delete a task | SRC-003 | Delete tasks so they no longer appear on the board. | Included High-Level Capabilities; Success Criteria | Covered | REQ-0001 / US-0003 | Single independently observable outcome |
| CAP-004 | Move a task between sections | SRC-004 | Move tasks between TODO, DOING, and DONE. | Included High-Level Capabilities; Success Criteria | Covered | REQ-0002 / US-0004 | Single independently observable outcome |
| CAP-005 | Display task-status counts | SRC-005 | Display basic counts for pending, current, and completed tasks. | Included High-Level Capabilities; Success Criteria | Covered | REQ-0003 / US-0005 | Single independently observable outcome |
| CAP-006 | Restore saved tasks and sections | SRC-006 | Preserve tasks and board state between browser sessions. | Included High-Level Capabilities; Success Criteria | Covered | REQ-0004 / US-0006 | Single independently observable outcome |

## 3. Requirements

## REQ-0001 — Manage task information

- **Status:** Approved
- **Source:** Approved Project Context
- **Evidence or basis:** Create, edit, and delete capabilities; recorded clarifications 1 through 3
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** The user must be able to create a task with a non-empty title, edit the title, and delete the task.
- **Approved by:** Product requester
- **Reviewer role or responsibility:** Product decision-maker
- **Approval date:** 2026-07-22
- **Blocking Issues or Feedback:** None

### US-0001 — Create a task

- **Status:** Approved
- **Source or evidence basis:** Approved Project Context and recorded clarifications 1 and 3
- **Covered scope IDs:** CAP-001
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to create a task with a title,  
so that I can record work to be done.

#### Acceptance Criteria

**Scenario: Create a task with a title**

Given the board is available  
When the user creates a task with a non-empty title  
Then the task is added to TODO with that title

### US-0002 — Edit a task title

- **Status:** Approved
- **Source or evidence basis:** Approved Project Context and recorded clarification 2
- **Covered scope IDs:** CAP-002
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to edit a task title,  
so that I can correct its information.

#### Acceptance Criteria

**Scenario: Save an edited title**

Given a task exists  
When the user replaces its title with another non-empty title  
Then the updated title is shown on the task

### US-0003 — Delete a task

- **Status:** Approved
- **Source or evidence basis:** Approved Project Context
- **Covered scope IDs:** CAP-003
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to delete a task,  
so that work I no longer need does not remain on the board.

#### Acceptance Criteria

**Scenario: Delete an existing task**

Given a task exists on the board  
When the user deletes the task  
Then the task no longer appears on the board

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** `python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync`
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## REQ-0002 — Organize tasks by status

- **Status:** Approved
- **Source:** Approved Project Context
- **Evidence or basis:** Move capability; recorded clarification 4
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** The user must be able to move a task between TODO, DOING, and DONE.
- **Approved by:** Product requester
- **Reviewer role or responsibility:** Product decision-maker
- **Approval date:** 2026-07-22
- **Blocking Issues or Feedback:** None

### US-0004 — Move a task

- **Status:** Approved
- **Source or evidence basis:** Approved Project Context and recorded clarification 4
- **Covered scope IDs:** CAP-004
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to move a task between sections,  
so that its section reflects its current status.

#### Acceptance Criteria

**Scenario: Move a task to another section**

Given a task exists in TODO  
When the user moves it to DOING  
Then it appears only in DOING

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** `python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync`
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## REQ-0003 — View task-status counts

- **Status:** Approved
- **Source:** Approved Project Context
- **Evidence or basis:** Status-count capability; recorded clarification 5
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** The board must display counts for TODO, DOING, and DONE as pending, current, and completed.
- **Approved by:** Product requester
- **Reviewer role or responsibility:** Product decision-maker
- **Approval date:** 2026-07-22
- **Blocking Issues or Feedback:** None

### US-0005 — View task-status counts

- **Status:** Approved
- **Source or evidence basis:** Approved Project Context and recorded clarification 5
- **Covered scope IDs:** CAP-005
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to view task-status counts,  
so that I can understand the state of my board.

#### Acceptance Criteria

**Scenario: View counts for every section**

Given tasks exist in TODO, DOING, and DONE  
When the board is displayed  
Then pending equals the TODO count, current equals the DOING count, and completed equals the DONE count

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** `python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync`
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## REQ-0004 — Preserve the board

- **Status:** Approved
- **Source:** Approved Project Context
- **Evidence or basis:** Persistence capability; recorded clarification 6
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** The board must preserve tasks and their sections between browser sessions.
- **Approved by:** Product requester
- **Reviewer role or responsibility:** Product decision-maker
- **Approval date:** 2026-07-22
- **Blocking Issues or Feedback:** None

### US-0006 — Restore the board

- **Status:** Approved
- **Source or evidence basis:** Approved Project Context and recorded clarification 6
- **Covered scope IDs:** CAP-006
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want my board restored when I return,  
so that I can continue my work.

#### Acceptance Criteria

**Scenario: Reopen the board**

Given tasks exist in different sections  
When the user closes and later reopens the application  
Then each task appears in its previous section

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 0
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Passed
- **Scope validator command:** `python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync`
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## 4. Approval Record

| Requirement | Decision | Approved by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
| REQ-0001 | Approved | Product requester | Product decision-maker | 2026-07-22 | None |
| REQ-0002 | Approved | Product requester | Product decision-maker | 2026-07-22 | None |
| REQ-0003 | Approved | Product requester | Product decision-maker | 2026-07-22 | None |
| REQ-0004 | Approved | Product requester | Product decision-maker | 2026-07-22 | None |
