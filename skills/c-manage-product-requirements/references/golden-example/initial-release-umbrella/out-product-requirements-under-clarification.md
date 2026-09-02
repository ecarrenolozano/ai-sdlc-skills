# Product Requirements

## 1. Document Control

- **Project:** Browser Task Board
- **Mode:** Initial release
- **Source project context or increment issue:** `sdlc_docs/00_inception/project_context.md`
- **Last updated:** 2026-07-23
- **Active scope state:** Under Clarification

## 2. Requirements Overview

| Requirement | Requirement status | Stories | Story status | Source | Repository issues |
|---|---|---|---|---|---|
| REQ-0001 Manage a personal browser task board | Under Clarification | US-0001, US-0002, US-0003, US-0004, US-0005, US-0006 | Draft | Approved Project Context | Not created |

### Source Statement Coverage Register

| Source ID | Source scope statement | Source location | Statement role | Decomposed into CAP IDs | Rationale |
|---|---|---|---|---|---|
| SRC-001 | Create and manage tasks on a personal board. | Project Context, Section 12, Included High-Level Capabilities | Umbrella | CAP-001, CAP-002, CAP-003, CAP-004 | Umbrella decomposition — “manage” is satisfied by the separately confirmed create, move, edit, and delete outcomes; no umbrella story is created. |
| SRC-002 | Move tasks between the three confirmed board sections. | Project Context, Section 12, Included High-Level Capabilities | Atomic | CAP-002 | One independently observable outcome. |
| SRC-003 | Edit and delete existing tasks. | Project Context, Section 12, Included High-Level Capabilities | Compound | CAP-003, CAP-004 | The statement contains two independent outcomes and is split into edit and delete. |
| SRC-004 | Preserve board state between browser sessions. | Project Context, Section 12, Included High-Level Capabilities | Atomic | CAP-005 | One independently observable outcome. |
| SRC-005 | Display basic task-status counts. | Project Context, Section 12, Included High-Level Capabilities | Atomic | CAP-006 | One independently observable outcome. |

### Source Scope Coverage Matrix

| Scope ID | Atomic capability | Source IDs | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|---|
| CAP-001 | Create a task on the personal board | SRC-001 | Create and manage tasks on a personal board. | Project Context, Section 12 | Pending clarification | REQ-0001 / US-0001 | Task information and initial board section require clarification. |
| CAP-002 | Move a task between TODO, DOING, and DONE | SRC-001, SRC-002 | Create and manage tasks on a personal board.; Move tasks between the three confirmed board sections. | Project Context, Section 12 | Covered | REQ-0001 / US-0002 | Single independently observable outcome. |
| CAP-003 | Edit an existing task | SRC-001, SRC-003 | Create and manage tasks on a personal board.; Edit and delete existing tasks. | Project Context, Section 12 | Pending clarification | REQ-0001 / US-0003 | Editable task information requires clarification. |
| CAP-004 | Delete an existing task | SRC-001, SRC-003 | Create and manage tasks on a personal board.; Edit and delete existing tasks. | Project Context, Section 12 | Covered | REQ-0001 / US-0004 | Single independently observable outcome. |
| CAP-005 | Restore saved board state between browser sessions | SRC-004 | Preserve board state between browser sessions. | Project Context, Section 12 | Covered | REQ-0001 / US-0005 | Single independently observable outcome. |
| CAP-006 | Display task-status counts | SRC-005 | Display basic task-status counts. | Project Context, Section 12 | Pending clarification | REQ-0001 / US-0006 | Count labels require clarification. |

## 3. Requirements

## REQ-0001 — Manage a personal browser task board

- **Status:** Under Clarification
- **Source:** Approved Project Context
- **Evidence or basis:** Approved Project Context and Source Statement Coverage Register SRC-001 through SRC-005.
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** The first release must let one user create, move, edit, delete, restore, and review status counts for tasks on a browser-based TODO, DOING, and DONE board.
- **Approved by:**
- **Reviewer role or responsibility:**
- **Approval date:**
- **Blocking Issues or Feedback:** Q1-Q3 remain open.

### Working Questions — Remove Before Approval

#### Q1

- **Question:** What task information must the first release support creating, displaying, and editing?
- **Status:** Open
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:** Needed for testable create and edit criteria without inventing task fields.

#### Q2

- **Question:** When a user creates a new task, which board section should it appear in first?
- **Status:** Open
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:** Needed for an observable create outcome.

#### Q3

- **Question:** Should counts map as pending = TODO, current = DOING, and completed = DONE?
- **Status:** Open
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:** Needed for supported status-count criteria.

### US-0001 — Create a task

- **Status:** Draft
- **Source or evidence basis:** SRC-001 / CAP-001.
- **Covered scope IDs:** CAP-001
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to create a task,  
so that I can record work on my personal board.

#### Acceptance Criteria

Pending clarification of task information and initial board section.

### US-0002 — Move a task between board sections

- **Status:** Draft
- **Source or evidence basis:** SRC-001, SRC-002 / CAP-002.
- **Covered scope IDs:** CAP-002
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to move a task between TODO, DOING, and DONE,  
so that its section reflects its current status.

#### Acceptance Criteria

**Scenario: Move a task**

Given a task exists in one board section  
When the user moves it to another board section  
Then the task appears in the selected section

### US-0003 — Edit a task

- **Status:** Draft
- **Source or evidence basis:** SRC-001, SRC-003 / CAP-003.
- **Covered scope IDs:** CAP-003
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to edit an existing task,  
so that its information remains accurate.

#### Acceptance Criteria

Pending clarification of editable task information.

### US-0004 — Delete a task

- **Status:** Draft
- **Source or evidence basis:** SRC-001, SRC-003 / CAP-004.
- **Covered scope IDs:** CAP-004
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to delete an existing task,  
so that it no longer appears on the board.

#### Acceptance Criteria

**Scenario: Delete a task**

Given a task exists on the board  
When the user deletes the task  
Then the task no longer appears on the board

### US-0005 — Restore saved board state

- **Status:** Draft
- **Source or evidence basis:** SRC-004 / CAP-005.
- **Covered scope IDs:** CAP-005
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want the saved board state restored when I return,  
so that I can continue my work.

#### Acceptance Criteria

**Scenario: Return to the saved board**

Given tasks exist in board sections  
When the user closes and later reopens the browser app  
Then the prior board state is available

### US-0006 — View task-status counts

- **Status:** Draft
- **Source or evidence basis:** SRC-005 / CAP-006.
- **Covered scope IDs:** CAP-006
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to view task-status counts,  
so that I can understand the state of my board.

#### Acceptance Criteria

Pending clarification of count labels and board-section mapping.

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 3
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Preflight passed
- **Scope validator command:** `python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md --mode initial-release --require-report-sync`
- **Scope validator report synchronized:** Yes
- **Validation result:** Failed — Q1-Q3 remain open and prevent Pending Approval.

## 4. Approval Record

| Requirement | Decision | Approved by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
| REQ-0001 | Pending clarification |  |  |  | Q1-Q3 open |
