# Product Requirements

## 1. Document Control

- **Project:** Personal Task Board
- **Mode:** Product increment
- **Source project context or increment issue:** Issue #90
- **Last updated:** 2026-07-22
- **Active scope state:** Approved

## 2. Requirements Overview

| Requirement | Requirement status | Stories | Story status | Source | Repository issues |
|---|---|---|---|---|---|
| REQ-0001 Manage tasks | Approved | US-0001 | Approved | Initial Project Context | #20 Open |
| REQ-0005 Filter tasks | Approved | US-0006 | Approved | Issue #90 | US #90 Open |

### Source Statement Coverage Register

| Source ID | Source scope statement | Source location | Statement role | Decomposed into CAP IDs | Rationale |
|---|---|---|---|---|---|
| SRC-001 | Filter tasks by priority. | Imported issue #90 and recorded refinement answers | Atomic | CAP-008 | Single independently observable source statement |

### Source Scope Coverage Matrix

| Scope ID | Atomic capability | Source IDs | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|---|
| CAP-008 | Filter visible tasks by one priority | SRC-001 | Filter tasks by priority. | Imported issue #90 and recorded refinement answers | Covered | REQ-0005 / US-0006 | Single independently observable outcome |

## 3. Requirements

## REQ-0005 — Filter tasks

- **Status:** Approved
- **Source:** Issue #90, classified as `user-story`
- **Evidence or basis:** Issue #90 and recorded refinement answers
- **Imported classification:** user-story
- **Repository representation:** Documentation only
- **Repository issue:** None — documentation only
- **Description:** The user must be able to limit the visible tasks to one selected priority.
- **Approved by:** Product requester
- **Reviewer role or responsibility:** Product decision-maker
- **Approval date:** 2026-07-22
- **Blocking Issues or Feedback:** None

### US-0006 — Filter tasks by priority

- **Status:** Approved
- **Source or evidence basis:** Issue #90 and recorded refinement answers
- **Covered scope IDs:** CAP-008
- **Atomicity:** Single observable outcome
- **Repository issue:** #90 Open

As a task-board user,  
I want to filter tasks by priority,  
so that I can focus on the most urgent work.

#### Acceptance Criteria

**Scenario: Select one priority**

Given tasks with different priorities exist  
When the user selects one priority  
Then only tasks with that priority are displayed

**Scenario: Clear the filter**

Given a priority filter is active  
When the user clears the filter  
Then all tasks are displayed

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
- **Scope validator command:** `python3 .agents/skills/c-manage-product-requirements/scripts/validate_scope_coverage.py <imported-source-artifact> sdlc_docs/01_requirements/product_requirements.md --mode product-increment --require-report-sync`
- **Scope validator report synchronized:** Yes
- **Validation result:** Passed

## 4. Approval Record

| Requirement | Decision | Approved by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
| REQ-0005 | Approved | Product requester | Product decision-maker | 2026-07-22 | None |
