# Product Requirements

## 1. Document Control

- **Project:** Browser Task Board
- **Mode:** Initial release
- **Source project context or increment issue:** `sdlc_docs/00_inception/project_context.md`
- **Last updated:** 2026-07-27
- **Active scope state:** Approved

## 2. Requirements Overview

| Requirement | Requirement status | Stories | Story status | Source | Repository issues |
|---|---|---|---|---|---|
| REQ-0001 Manage a personal browser task board | Approved | US-0001, US-0002, US-0003, US-0004, US-0005, US-0006 | Approved | Approved Project Context and recorded stakeholder answers | Created |

### Source Statement Coverage Register

| Source ID | Source scope statement | Source location | Statement role | Decomposed into CAP IDs | Rationale |
|---|---|---|---|---|---|
| SRC-001 | Create and manage tasks on a personal board. | Project Context, Section 12, Included High-Level Capabilities | Umbrella | CAP-001, CAP-002, CAP-003, CAP-004 | Umbrella decomposition - "manage" is satisfied by the separately confirmed create, move, edit, and delete outcomes; no umbrella story is created. |
| SRC-002 | Move tasks between the three confirmed board sections. | Project Context, Section 12, Included High-Level Capabilities | Atomic | CAP-002 | One independently observable source statement. |
| SRC-003 | Edit and delete existing tasks. | Project Context, Section 12, Included High-Level Capabilities | Compound | CAP-003, CAP-004 | The statement contains two independently observable outcomes and is split into edit and delete. |
| SRC-004 | Preserve board state between browser sessions. | Project Context, Section 12, Included High-Level Capabilities | Atomic | CAP-005 | One independently observable source statement. |
| SRC-005 | Display basic task-status counts. | Project Context, Section 12, Included High-Level Capabilities | Atomic | CAP-006 | One independently observable source statement. |

### Source Scope Coverage Matrix

| Scope ID | Atomic capability | Source IDs | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|---|
| CAP-001 | Create a task on the personal board | SRC-001 | Create and manage tasks on a personal board. | Project Context, Section 12 | Covered | REQ-0001 / US-0001 | Stakeholder answer: tasks require a title, may include a description, and new tasks start in TODO. |
| CAP-002 | Move a task between TODO, DOING, and DONE | SRC-001, SRC-002 | Create and manage tasks on a personal board.; Move tasks between the three confirmed board sections. | Project Context, Section 12 | Covered | REQ-0001 / US-0002 | Single independently observable outcome. |
| CAP-003 | Edit an existing task | SRC-001, SRC-003 | Create and manage tasks on a personal board.; Edit and delete existing tasks. | Project Context, Section 12 | Covered | REQ-0001 / US-0003 | Stakeholder answer: task title and description must be editable. |
| CAP-004 | Delete an existing task | SRC-001, SRC-003 | Create and manage tasks on a personal board.; Edit and delete existing tasks. | Project Context, Section 12 | Covered | REQ-0001 / US-0004 | Single independently observable outcome. |
| CAP-005 | Restore saved board state between browser sessions | SRC-004 | Preserve board state between browser sessions. | Project Context, Section 12 | Covered | REQ-0001 / US-0005 | Single independently observable outcome. |
| CAP-006 | Display task-status counts | SRC-005 | Display basic task-status counts. | Project Context, Section 12 | Covered | REQ-0001 / US-0006 | Stakeholder answer: pending maps to TODO, current maps to DOING, and completed maps to DONE. |

## 3. Requirements

## REQ-0001 — Manage a personal browser task board

- **Status:** Approved
- **Source:** Approved Project Context
- **Evidence or basis:** Approved Project Context, Source Statement Coverage Register SRC-001 through SRC-005, and stakeholder answers recorded during Product Requirements Management on 2026-07-23.
- **Imported classification:** Not applicable
- **Repository representation:** Created
- **Repository issue:** Created
- **Description:** The first release must let one user create tasks with a required title and optional description, display both task fields, move tasks between TODO, DOING, and DONE, edit task title and description, delete tasks, restore saved board state, and view status counts for pending, current, and completed tasks.
- **Approved by:** Edwin Carreno
- **Reviewer role or responsibility:** SSC Developer
- **Approval date:** 2026-07-23
- **Blocking Issues or Feedback:** None

### Recorded Clarification Evidence

| Question | Answered by | Evidence source | Answer | Impact |
|---|---|---|---|---|
| What task information must the first release support creating, displaying, and editing? | Edwin Carreno | Stakeholder answer in Product Requirements Management, 2026-07-23 | Each task must have a required title and an optional description. Both fields must be displayed, and the user must be able to edit them. | Supports create, display, and edit acceptance criteria. |
| When a user creates a new task, which board section should it appear in first? | Edwin Carreno | Stakeholder answer in Product Requirements Management, 2026-07-23 | Every newly created task must initially appear in the TODO section. | Supports the observable create outcome. |
| Should counts map as pending = TODO, current = DOING, and completed = DONE? | Edwin Carreno | Stakeholder answer in Product Requirements Management, 2026-07-23 | Yes. The counts map directly as pending = TODO, current = DOING, and completed = DONE. | Supports the status-count acceptance criterion. |

### US-0001 — Create a task

- **Status:** Approved
- **Source or evidence basis:** SRC-001 / CAP-001; stakeholder answers recorded during Product Requirements Management on 2026-07-23.
- **Covered scope IDs:** CAP-001
- **Atomicity:** Single observable outcome
- **Repository issue:** Created

As a task-board user,  
I want to create a task with a title and optional description,  
so that I can record work on my personal board.

#### Acceptance Criteria

**Scenario: Create a task with required task information**

Given the board is available  
When the user creates a task with a title and optional description  
Then the task appears in TODO with its title and description displayed

### US-0002 — Move a task between board sections

- **Status:** Approved
- **Source or evidence basis:** SRC-001, SRC-002 / CAP-002.
- **Covered scope IDs:** CAP-002
- **Atomicity:** Single observable outcome
- **Repository issue:** Created

As a task-board user,  
I want to move a task between TODO, DOING, and DONE by dragging and dropping it,
so that its section reflects its current status.

#### Acceptance Criteria

**Scenario: Drag and drop a task between board sections**

Given a task exists in one board section  
When the user drags and drops it into another board section
Then the task appears in the selected section

### US-0003 — Edit a task

- **Status:** Approved
- **Source or evidence basis:** SRC-001, SRC-003 / CAP-003; stakeholder answer recorded during Product Requirements Management on 2026-07-23.
- **Covered scope IDs:** CAP-003
- **Atomicity:** Single observable outcome
- **Repository issue:** Created

As a task-board user,  
I want to edit an existing task's title and description,  
so that its information remains accurate.

#### Acceptance Criteria

**Scenario: Edit task information**

Given a task exists with a title and description  
When the user edits the task title or description  
Then the updated title and description are displayed on the task

### US-0004 — Delete a task

- **Status:** Approved
- **Source or evidence basis:** SRC-001, SRC-003 / CAP-004.
- **Covered scope IDs:** CAP-004
- **Atomicity:** Single observable outcome
- **Repository issue:** Created

As a task-board user,  
I want to delete an existing task,  
so that it no longer appears on the board.

#### Acceptance Criteria

**Scenario: Delete a task**

Given a task exists on the board  
When the user deletes the task  
Then the task no longer appears on the board

### US-0005 — Restore saved board state

- **Status:** Approved
- **Source or evidence basis:** SRC-004 / CAP-005.
- **Covered scope IDs:** CAP-005
- **Atomicity:** Single observable outcome
- **Repository issue:** Created

As a task-board user,  
I want the saved board state restored when I return,  
so that I can continue my work.

#### Acceptance Criteria

**Scenario: Return to the saved board**

Given tasks exist in board sections  
When the user closes and later reopens the browser app  
Then the prior board state is available

### US-0006 — View task-status counts

- **Status:** Approved
- **Source or evidence basis:** SRC-005 / CAP-006; stakeholder answer recorded during Product Requirements Management on 2026-07-23.
- **Covered scope IDs:** CAP-006
- **Atomicity:** Single observable outcome
- **Repository issue:** Created

As a task-board user,  
I want to view task-status counts,  
so that I can understand the state of my board.

#### Acceptance Criteria

**Scenario: View mapped task-status counts**

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

## 4. Approval Record

| Requirement | Decision | Approved by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
| REQ-0001 | Approved | Edwin Carreno | SSC Developer | 2026-07-23 | None |
