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
| REQ-0001 Manage a personal browser task board | Under Clarification | US-0001, US-0002, US-0003, US-0004, US-0005, US-0006, US-0007 | Draft | Approved Project Context | Not created |

### Source Scope Coverage Matrix

| Scope ID | Atomic capability | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|
| CAP-001 | Create tasks on a personal board | Create and manage tasks on a personal board. | Project Context, Section 12, MVP Boundary, Included High-Level Capabilities | Pending clarification | REQ-0001 / US-0001 | Requires stakeholder clarification of task information and initial task section |
| CAP-002 | Manage existing tasks on a personal board | Create and manage tasks on a personal board. | Project Context, Section 12, MVP Boundary, Included High-Level Capabilities | Pending clarification | REQ-0001 / US-0002 | Requires stakeholder confirmation that create, move, edit, and delete fully express the intended management actions |
| CAP-003 | Move tasks between TODO, DOING, and DONE | Move tasks between the three confirmed board sections. | Project Context, Section 12, MVP Boundary, Included High-Level Capabilities | Covered | REQ-0001 / US-0003 | Single independently observable outcome |
| CAP-004 | Edit existing tasks | Edit and delete existing tasks. | Project Context, Section 12, MVP Boundary, Included High-Level Capabilities | Pending clarification | REQ-0001 / US-0004 | Requires stakeholder clarification of editable task information |
| CAP-005 | Delete existing tasks | Edit and delete existing tasks. | Project Context, Section 12, MVP Boundary, Included High-Level Capabilities | Covered | REQ-0001 / US-0005 | Single independently observable outcome |
| CAP-006 | Preserve board state between browser sessions | Preserve board state between browser sessions. | Project Context, Section 12, MVP Boundary, Included High-Level Capabilities | Covered | REQ-0001 / US-0006 | Single independently observable outcome |
| CAP-007 | Display basic task-status counts | Display basic task-status counts. | Project Context, Section 12, MVP Boundary, Included High-Level Capabilities | Pending clarification | REQ-0001 / US-0007 | Requires stakeholder clarification of how pending, current, and completed counts map to board sections |

Allowed dispositions:

- `Covered`
- `Grouped`
- `Pending clarification`
- `Deferred by approved decision`
- `Excluded by approved decision`

## 3. Requirements

## REQ-0001 — Manage a personal browser task board

- **Status:** Under Clarification
- **Source:** Approved Project Context
- **Evidence or basis:** The approved Project Context states that the first release is for a single user and includes creating and managing tasks on a personal board, moving tasks between TODO, DOING, and DONE, editing and deleting tasks, preserving board state between browser sessions, and displaying basic task-status counts.
- **Imported classification:** Not applicable
- **Repository representation:** Not created
- **Repository issue:** Not created
- **Description:** The first release must let a single user manage a browser-based TODO, DOING, and DONE task board within the approved lightweight scope.
- **Approved by:**
- **Reviewer role or responsibility:**
- **Approval date:**
- **Blocking Issues or Feedback:**

### Working Questions — Remove Before Approval

#### Q1

- **Question:** What task information must the first release support creating, displaying, and editing?
- **Status:** Open
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:** Needed to write testable create and edit acceptance criteria without inventing task fields.

#### Q2

- **Question:** When a user creates a new task, which board section should it appear in first?
- **Status:** Open
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:** Needed to make task creation observable and testable.

#### Q3

- **Question:** Does "manage tasks on a personal board" mean only create, move, edit, and delete for the first release, or is another user-observable task action required?
- **Status:** Open
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:** Needed to finalize the disposition for CAP-002 without silently omitting or inventing a management action.

#### Q4

- **Question:** Should the simple counts map directly as pending = TODO, current = DOING, and completed = DONE?
- **Status:** Open
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:** Needed to write supported acceptance criteria for task-status counts.

### US-0001 — Create a task

- **Status:** Draft
- **Source or evidence basis:** Approved Project Context, Section 12, Included High-Level Capabilities: "Create and manage tasks on a personal board."
- **Covered scope IDs:** CAP-001
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to create a task,  
so that I can record work on my personal board.

#### Acceptance Criteria

Pending clarification of required task information and the initial board section for new tasks.

### US-0002 — Manage existing tasks

- **Status:** Draft
- **Source or evidence basis:** Approved Project Context, Section 12, Included High-Level Capabilities: "Create and manage tasks on a personal board."
- **Covered scope IDs:** CAP-002
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to manage existing tasks on my personal board,  
so that the board reflects my current work.

#### Acceptance Criteria

Pending clarification of whether create, move, edit, and delete fully express the first-release task management actions.

### US-0003 — Move a task between board sections

- **Status:** Draft
- **Source or evidence basis:** Approved Project Context, Section 12, Included High-Level Capabilities: "Move tasks between the three confirmed board sections."
- **Covered scope IDs:** CAP-003
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to move a task between TODO, DOING, and DONE,  
so that its board section reflects its current status.

#### Acceptance Criteria

**Scenario: Move a task to another section**

Given a task exists in one board section  
When the user moves it to another board section  
Then the task appears in the new section

### US-0004 — Edit a task

- **Status:** Draft
- **Source or evidence basis:** Approved Project Context, Section 12, Included High-Level Capabilities: "Edit and delete existing tasks."
- **Covered scope IDs:** CAP-004
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to edit an existing task,  
so that I can keep its information accurate.

#### Acceptance Criteria

Pending clarification of required editable task information.

### US-0005 — Delete a task

- **Status:** Draft
- **Source or evidence basis:** Approved Project Context, Section 12, Included High-Level Capabilities: "Edit and delete existing tasks."; Section 17, Success Criteria: "Deleted tasks no longer appear on the board."
- **Covered scope IDs:** CAP-005
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to delete an existing task,  
so that it no longer appears on my board.

#### Acceptance Criteria

**Scenario: Delete an existing task**

Given a task exists on the board  
When the user deletes the task  
Then the task no longer appears on the board

### US-0006 — Restore saved board state

- **Status:** Draft
- **Source or evidence basis:** Approved Project Context, Section 12, Included High-Level Capabilities: "Preserve board state between browser sessions."
- **Covered scope IDs:** CAP-006
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want my board state preserved between browser sessions,  
so that I can return later to the saved board.

#### Acceptance Criteria

**Scenario: Return to the saved board**

Given the board has tasks arranged across board sections  
When the user closes and later reopens the browser app  
Then the board state is available from the prior session

### US-0007 — View task-status counts

- **Status:** Draft
- **Source or evidence basis:** Approved Project Context, Section 12, Included High-Level Capabilities: "Display basic task-status counts."; Section 9, Expected Outcomes: "The user can see simple counts for pending, current, and completed tasks."
- **Covered scope IDs:** CAP-007
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to view basic task-status counts,  
so that I can understand the state of my board.

#### Acceptance Criteria

Pending clarification of how pending, current, and completed counts map to board sections.

### Requirement Validation

- **Source evidence recorded:** Yes
- **Approved content changed:** No
- **Source scope statements omitted:** 0
- **Atomic capabilities without disposition:** 0
- **Compound stories without approved grouping:** 0
- **Coverage matrix/story mapping conflicts:** 0
- **Unsupported product behavior:** 0
- **Unresolved blocking questions:** 4
- **Duplicate repository story references:** 0
- **Overview/detail inconsistencies:** 0
- **Scope coverage validator:** Not run — stopped at first required stakeholder question round before requesting approval.
- **Validation result:** Failed — unresolved blocking questions prevent Pending Approval.

## 4. Approval Record

| Requirement | Decision | Approved by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
| REQ-0001 | Pending clarification |  |  |  | Q1-Q4 open |

