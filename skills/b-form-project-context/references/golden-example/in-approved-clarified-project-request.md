# Golden Example — Clarified Project Request

## 1. Source

- **Original document:** `sources/00-informal-project-request.md`
- **Requester:** Robert Bosch
- **Date received:** 2026-07-22
- **Source type:** Email
- **Prepared by:** Edwin Carreño
- **Document state:** Closed

## 2. Initial Understanding

### Summary

Currently, Robert Bosch manages his personal activities without a single visual workflow that clearly shows which tasks are pending, in progress, or completed. He wants a browser-based application that provides one personal task board with three fixed sections: `TODO`, `DOING`, and `DONE`, so that he can organize his activities and follow their progress more easily.

The first usable version must be available within one week. It is intended for a single user and must support creating, editing, deleting, and moving tasks between the three sections. Tasks must remain available after the browser is closed and reopened.

Authentication, collaboration, multiple boards, configurable sections, notifications, task deadlines, priorities, labels, attachments, and native mobile or desktop applications are outside the initial project boundary.

## 3. Critical Questions

### Q1 — Problem or current situation

- **Question:** What difficulty are you currently experiencing when managing your activities?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester
- **Answer:** I currently use notes and memory to track my activities. It is difficult to see which tasks are pending, which ones I am actively working on, and which ones are already complete.
- **Impact:** The project addresses the lack of a single visual workflow for organizing personal activities and tracking their status. Team coordination and project portfolio management are not part of the identified problem.

### Q2 — Expected outcome

- **Question:** What must the first usable version of the application allow you to do?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester
- **Answer:** I need to create tasks, update them, delete them, and move them between `TODO`, `DOING`, and `DONE`. My tasks must still be available when I close the browser and return later.
- **Impact:** The first usable version must support the basic task lifecycle and persistent storage. The storage technology and detailed interaction design remain decisions for later requirements and architecture activities.

### Q3 — Users or beneficiaries

- **Question:** Who will use the first version of the application?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester
- **Answer:** I will be the only user of the first version. The application is for managing my personal activities.
- **Impact:** The initial project is a single-user application. Authentication, account management, shared boards, user roles, permissions, and collaboration are excluded from the initial project boundary.

### Q4 — Initial project boundary

- **Question:** What should be excluded from the first usable version?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester
- **Answer:** The first version does not need authentication, collaboration, multiple boards, configurable sections, notifications, task deadlines, priorities, labels, attachments, or a mobile application.
- **Impact:** The initial project is limited to one personal board with three fixed sections and basic task management. The excluded capabilities must not be treated as current project requirements.

### Q5 — Constraint or deadline

- **Question:** When must the first usable version of the application be available?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester and Project Owner
- **Answer:** The first usable version must be available within one week.
- **Impact:** The project has a fixed one-week deadline. The initial delivery must remain focused on the agreed core capabilities.

### Q6 — Product boundary

- **Question:** Are the three board sections fixed, or should the user be able to rename, remove, or add sections?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester
- **Answer:** The three sections are fixed. I do not need to rename them, remove them, or create additional sections.
- **Impact:** The initial board contains exactly three fixed sections: `TODO`, `DOING`, and `DONE`. Configurable workflows are excluded.

### Q7 — Project rationale

- **Question:** Why is this application needed now?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester and Project Owner
- **Answer:** My current use of notes and memory is already causing me to overlook pending tasks and lose track of work in progress. I need a simple replacement immediately.
- **Impact:** The project responds to an immediate personal organization problem rather than a long-term team product initiative.

### Q8 — Project success

- **Question:** How will you determine whether the first usable version has achieved its intended result?
- **Status:** Answered
- **Answered by:** Robert Bosch, Requester and Project Owner
- **Answer:** I will consider it successful if I can use one board to manage my personal tasks, see their status, move them through the three sections, return later without losing them, and stop relying on separate notes.
- **Impact:** Project-level success is defined by replacing the requester's fragmented task-tracking method with one persistent visual workflow.

## 4. Readiness Approval

### Status

- [x] Ready
- [ ] Not Ready

### Approved by

- **Name:** Robert Bosch
- **Role:** Requester and Project Owner
- **Date:** 2026-07-22

### Blocking Issues

None.

### Approval Rule

The document can be passed to `b-form-project-context` only when:

- `Ready` is selected.
- The approver name, role, and date are recorded.
- `Blocking Issues` is `None`.


## 5. Later Stakeholder Clarification

- **Date:** 2026-07-23
- **Provided by:** Robert Bosch, Requester and Project Owner
- **Clarification:** Future collaboration is a future design consideration. It is not included in the first-release scope, and it must not be translated into current collaboration features or a prescribed technical architecture.
- **Classification impact:** Promote the future-collaboration statement from a derived interpretation to an `Approved decision`.
