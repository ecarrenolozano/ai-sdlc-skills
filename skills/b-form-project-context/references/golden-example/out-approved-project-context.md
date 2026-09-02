# Golden Example — Project Context

> This fictional example demonstrates a valid approved output. It is not project evidence and must never be copied as factual content into another project.

## 1. Document Control

- **Project name:** Personal Task Board
- **Source request:** `clarified_project_request.md`
- **Prepared by:** Edwin Carreño
- **Version:** 1.1
- **Last updated:** 2026-07-23
- **Document state:** Closed

## 2. Project Summary

The Personal Task Board project will provide Robert Bosch with a browser-based application for managing personal tasks on one persistent board with three fixed sections: `TODO`, `DOING`, and `DONE`. The approved first version is for one user, must support the basic task lifecycle, and must be available within one week.

## 3. Evidence and Classification Register

| Statement | Classification | Evidence or basis | Confirmation path if unconfirmed |
|---|---|---|---|
| Robert is the only intended user of the first version. | Confirmed fact | Clarified Request, Q3 | — |
| Tasks must remain available after the browser is closed and reopened. | Confirmed fact | Clarified Request, Q2 | — |
| The board has exactly `TODO`, `DOING`, and `DONE`. | Approved decision | Clarified Request, Q6 | — |
| Future collaborative boards are a design consideration for later evolution, not part of the first-release scope. | Approved decision | Later Stakeholder Clarification, 2026-07-23 | — |
| The first useful version must be available within one week. | Confirmed fact | Clarified Request, Q5 | — |
| Scope growth could threaten the one-week delivery. | Derived interpretation | One-week deadline in Q5 plus explicit exclusions in Q4 | — |
| The person responsible for building the software is unknown. | Open question | No builder responsibility is assigned in the approved source | Confirm during planning if required |

## 4. Background

Robert currently uses separate notes and memory to manage personal activities. He reported difficulty distinguishing pending, active, and completed work and said that he overlooks pending tasks and loses track of work in progress.

## 5. Problem Statement

Robert does not have one persistent visual place for organizing personal tasks by status. He therefore relies on separate notes and memory and has limited visibility into pending, active, and completed work.

## 6. Why the Project Is Needed

The current approach is already causing Robert to overlook tasks and lose track of ongoing work. He requested a simple replacement, with a first usable version within one week.

## 7. Desired Future Situation

Robert can open one board in a web browser, see the status of his personal tasks, move them through the supported workflow, and return later without losing them.

## 8. Project Goal

Deliver within one week a browser-based personal task board that supports the approved task lifecycle across `TODO`, `DOING`, and `DONE` and retains tasks between browser sessions.

## 9. Expected Outcomes

- Robert has one visual place for tracking personal tasks.
- Pending, in-progress, and completed tasks are clearly separated.
- Tasks remain available between browser sessions.
- Robert can use the supported workflow without relying on separate notes for it.

## 10. People Involved

### Intended Users

- Robert Bosch, the only user of the first version.

### Other People Affected

- Not identified in the approved source.

### Confirmed Responsibilities

- **Robert Bosch:** Requested the project, defines the intended result, makes project-level decisions, and confirms whether the delivered software meets the agreed scope. Evidence: Clarified Request Q3, Q5, Q7, Q8, and approval record.
- **Edwin Carreño:** Prepared the inception documents. Evidence: source metadata.

## 11. High-Level Scope

### Included

- One browser-based personal task board.
- Three fixed sections: `TODO`, `DOING`, and `DONE`.
- Creating, editing, deleting, and moving personal tasks.
- Preserving tasks between browser sessions.
- Delivery of the first useful version within one week.

### Excluded

- Authentication and user accounts.
- Multiple users, shared boards, and collaboration.
- Multiple boards or configurable sections.
- Notifications, task deadlines, priorities, labels, and attachments.
- Native mobile or desktop applications.
- Team coordination and project portfolio management.

### Future Design Considerations

- Avoid project-level decisions that would unnecessarily prevent later collaborative-board support.
  - **Classification:** Approved decision
  - **Evidence:** Later Stakeholder Clarification, 2026-07-23.


## 12. MVP Boundary

### Intended User

Robert Bosch.

### Minimum Useful Outcome

Robert can manage the approved personal-task workflow on one persistent visual board instead of using separate notes and memory.

### Included High-Level Capabilities

- Create, edit, and delete personal tasks.
- View tasks in the three fixed sections.
- Move tasks between sections.
- Retain tasks between browser sessions.

### Explicitly Excluded

- Authentication, multiple users, and collaboration.
- Multiple boards and configurable sections.
- Notifications and advanced task information.
- Native applications.

### Confirmed Delivery Limits

- The first useful version must be available within one week.
- The software must run in a web browser.
- The first version supports one user and one board.
- The board contains exactly three fixed sections.

### Completion Condition

The approved first-version scope is delivered when Robert can create, edit, delete, view, move, and retain personal tasks on one browser-based board with the three fixed sections.

## 13. Constraints

- One-week delivery deadline.
- Browser-based operation.
- One user and one board in the first version.
- Exactly three fixed workflow sections.

## 14. Assumptions

No assumptions recorded.

## 15. Dependencies

No dependencies identified in the approved source.

## 16. Risks and Uncertainties

- **Scope growth could threaten the deadline:** Additional capabilities may prevent delivery within one week.
  - **Classification:** Derived interpretation
  - **Evidence or basis:** Confirmed one-week deadline and explicit first-version exclusions.
  - **Affected project area:** Schedule and first-release scope.
- **Detailed behavior remains undefined:** Product Requirements Management must define observable behavior and acceptance conditions for the approved high-level capabilities.
  - **Classification:** Derived interpretation
  - **Evidence or basis:** The approved source defines capabilities at project level but intentionally does not contain detailed requirements.
  - **Affected project area:** Product Requirements Management.
- **Builder responsibility is unknown:** Planning may be blocked if assigning implementation responsibility becomes necessary.
  - **Classification:** Open question
  - **Evidence or basis:** No builder is assigned in the approved source.
  - **Affected project area:** Planning and responsibility assignment.

## 17. Success Criteria

- A first useful version is available within one week.
- Robert can create, edit, delete, and view personal tasks on one board.
- Robert can move tasks between `TODO`, `DOING`, and `DONE`.
- Tasks remain available after the browser is closed and reopened.
- Robert confirms that the delivered software supports the agreed workflow without requiring separate notes for that workflow.

## 18. Confirmed Decisions and Responsibilities

- **Person who requested the project:** Robert Bosch
- **Person who makes project-level decisions:** Robert Bosch
- **Person who confirms the software meets the agreed scope:** Robert Bosch
- **Person responsible for building the software:** Not assigned in the approved source

## 19. Validation Report

- **Approved source modified:** No
- **Unsupported confirmed claims:** 0
- **Derived interpretations without basis:** 0
- **Classification conflicts across sections:** 0
- **Mixed confirmed-and-derived statements:** 0
- **Stakeholder-confirmed interpretations not promoted:** 0
- **Assumptions without confirmation path:** 0
- **Open questions presented as resolved:** 0
- **Scope contradictions:** 0
- **Premature downstream detail:** 0
- **Authorized traceability fields changed:** `Project context`: Status, Current activity, Evidence, Missing or blocked, Next action; `Initial requirements`: Current activity, Evidence, Missing or blocked, Next action
- **Unauthorized traceability changes detected:** 0
- **Traceability Mutation Guard:** Passed
- **Working Questions remaining:** 0
- **Blocking validation failures:** None

## 20. Project Context Approval

### Status

- [x] Ready for Product Requirements
- [ ] Not Ready

### Reviewed by

- **Name:** Robert Bosch
- **Role or responsibility:** Requested the project and makes project-level decisions
- **Date:** 2026-07-23

### Blocking Issues or Feedback

None.

### Approval Rule

The document can be closed and passed to `c-manage-product-requirements` only when:

- Exactly one decision is selected.
- `Ready for Product Requirements` is selected.
- Reviewer name, role or responsibility, and date are recorded.
- `Blocking Issues or Feedback` is `None`.
