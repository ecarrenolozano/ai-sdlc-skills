# Product Requirements

## 1. Document Control

- **Project:**
- **Mode:** Initial release | Product increment
- **Source project context or increment issue:**
- **Last updated:**
- **Active scope state:** Draft | Under Clarification | Pending Approval | Approved

## 2. Requirements Overview

| Requirement | Requirement status | Stories | Story status | Source | Repository issues |
|---|---|---|---|---|---|

### Source Statement Coverage Register

Record every controlling source statement exactly once. Classify broad category statements such as “manage”, “handle”, or “support” as `Umbrella`; do not create an umbrella capability or story from them.

| Source ID | Source scope statement | Source location | Statement role | Decomposed into CAP IDs | Rationale |
|---|---|---|---|---|---|
| SRC-001 |  |  | Atomic | CAP-001 |  |

Allowed statement roles:

- `Atomic`: exactly one independently observable outcome and one CAP ID.
- `Compound`: multiple independent outcomes and at least two CAP IDs.
- `Umbrella`: a broad category decomposed into concrete CAP IDs; begin the rationale with `Umbrella decomposition —`.

### Source Scope Coverage Matrix

Record only atomic capabilities. Every row must reference one or more Source IDs from the register. Never use an umbrella verb as the atomic capability.

| Scope ID | Atomic capability | Source IDs | Source scope statement | Source location | Disposition | Requirement / Stories | Rationale or approval evidence |
|---|---|---|---|---|---|---|---|
| CAP-001 |  | SRC-001 |  |  | Covered | REQ-0001 / US-0001 | Single independently observable outcome |

Allowed dispositions:

- `Covered`
- `Grouped`
- `Pending clarification`
- `Deferred by approved decision`
- `Excluded by approved decision`

Use `Grouped` only when a human explicitly approves combining independently observable outcomes. Begin the rationale with `Approved grouping —` and record the evidence.

## 3. Requirements

## REQ-0001 — Requirement title

- **Status:** Unapproved
- **Source:**
- **Evidence or basis:**
- **Imported classification:** Not applicable | broad-request | user-story
- **Repository representation:** Not created | Broad original issue | Documentation only
- **Repository issue:**
- **Description:**
- **Approved by:**
- **Reviewer role or responsibility:**
- **Approval date:**
- **Blocking Issues or Feedback:**

### Working Questions — Remove Before Approval

Include only while this requirement is under clarification. Ask one small round and stop.

#### Q1

- **Question:**
- **Status:** Open | Answered
- **Answered by:**
- **Evidence source:**
- **Answer:**
- **Impact:**

### US-0001 — Story title

- **Status:** Draft
- **Source or evidence basis:**
- **Covered scope IDs:** CAP-001
- **Atomicity:** Single observable outcome | Approved grouping — [rationale and approval evidence]
- **Repository issue:**

As a ...  
I want ...  
so that ...

#### Acceptance Criteria

**Scenario: Observable outcome**

Given ...  
When ...  
Then ...

### Requirement Validation

- **Source evidence recorded:** Yes | No
- **Approved content changed:** No | Yes — [details]
- **Source scope statements omitted:** 0 | [details]
- **Atomic capabilities without disposition:** 0 | [details]
- **Compound stories without approved grouping:** 0 | [details]
- **Coverage matrix/story mapping conflicts:** 0 | [details]
- **Unsupported product behavior:** 0 | [details]
- **Unresolved blocking questions:** 0 | [details]
- **Duplicate repository story references:** 0 | [details]
- **Overview/detail inconsistencies:** 0 | [details]
- **Scope coverage validator:** Not run | Preflight passed | Passed | Failed — [details]
- **Scope validator command:**
- **Scope validator report synchronized:** No | Yes
- **Validation result:** Passed | Failed — [details]

## 4. Approval Record

| Requirement | Decision | Approved by | Role or responsibility | Date | Blocking Issues or Feedback |
|---|---|---|---|---|---|
