# Product Requirements

## 1. Document Control

- **Project:** Personal Task Board
- **Mode:** Product increment
- **Source project context or increment issue:** Issue #84
- **Last updated:** 2026-07-22
- **Active scope state:** Approved

## 2. Requirements Overview

| Requirement | Requirement status | Stories | Story status | Source | Repository issues |
|---|---|---|---|---|---|
| REQ-0001 Manage tasks | Approved | US-0001 | Approved | Initial Project Context | #20 Open |
| REQ-0004 Export tasks | Approved | US-0005 | Approved | Issue #84 | REQ #84 Open; US not created |

### Source Statement Coverage Register

| Source ID | Source scope statement | Source location | Statement role | Decomposed into CAP IDs | Rationale |
|---|---|---|---|---|---|
| SRC-001 | Export the current task list as a CSV file. | Imported issue #84 and recorded refinement answers | Atomic | CAP-007 | Single independently observable source statement |

### Source Scope Coverage Matrix

| Scope ID | Atomic capability | Source IDs | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|---|
| CAP-007 | Export the current task list as CSV | SRC-001 | Export the current task list as a CSV file. | Imported issue #84 and recorded refinement answers | Covered | REQ-0004 / US-0005 | Single independently observable outcome |

## 3. Requirements

## REQ-0004 — Export tasks

- **Status:** Approved
- **Source:** Issue #84, classified as `broad-request`
- **Evidence or basis:** Issue #84 and recorded refinement answers
- **Imported classification:** broad-request
- **Repository representation:** Broad original issue
- **Repository issue:** #84 Open
- **Description:** The user must be able to export the current task list as a CSV file containing title and status.
- **Approved by:** Product requester
- **Reviewer role or responsibility:** Product decision-maker
- **Approval date:** 2026-07-22
- **Blocking Issues or Feedback:** None

### US-0005 — Export tasks as CSV

- **Status:** Approved
- **Source or evidence basis:** Issue #84 and recorded refinement answers
- **Covered scope IDs:** CAP-007
- **Atomicity:** Single observable outcome
- **Repository issue:** Not created

As a task-board user,  
I want to export my tasks as CSV,  
so that I can use the task list outside the application.

#### Acceptance Criteria

**Scenario: Export current tasks**

Given the board contains tasks  
When the user exports the board  
Then a CSV file is downloaded  
And it contains each task title and current status

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
| REQ-0004 | Approved | Product requester | Product decision-maker | 2026-07-22 | None |
