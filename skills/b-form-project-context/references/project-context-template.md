# Project Context

## How to Use This Document

This document turns an approved Clarified Project Request into an evidence-grounded, high-level definition of the software project.

Rules:

1. Verify that the source request is closed, ready, fully approved, and has no blocking issues.
2. Use only approved evidence and recorded stakeholder answers as confirmed facts.
3. Classify substantive information as `Confirmed fact`, `Derived interpretation`, `Assumption`, `Open question`, or `Approved decision`.
4. Record evidence for confirmed facts, derived interpretations, and approved decisions.
5. Never silently fill a gap. Use `Not identified in the approved source` for non-blocking gaps.
6. Ask no more than 20 distinct Working Questions across the document lifecycle.
7. Ask questions in small rounds, normally one to four, and stop until answers are available.
8. Remove Working Questions before approval.
9. Do not include detailed requirements, user stories, architecture, implementation plans, repository issues, or test plans.
10. Close the document only after valid human approval as `Ready for Product Requirements`.

---

## 1. Document Control

- **Project name:** [Project name]
- **Source request:** `clarified_project_request.md`
- **Prepared by:** [Name]
- **Version:** [Version]
- **Last updated:** [YYYY-MM-DD]
- **Document state:** Draft | Under Clarification | Pending Approval | Closed

## 2. Project Summary

[Summarize the problem, intended user, expected result, first useful software version, and main confirmed limit in one concise paragraph.]

## 3. Evidence and Classification Register

Record substantive statements that materially shape the Project Context.

| Statement | Classification | Evidence or basis | Confirmation path if unconfirmed |
|---|---|---|---|
| [Statement] | Confirmed fact | [Approved source section or recorded answer] | — |
| [Statement] | Derived interpretation | [Confirmed facts and reasoning basis] | — |
| [Statement] | Assumption | [Why it is temporarily needed] | [Who or what must confirm it] |
| [Statement] | Open question | [Why the information matters] | [Who should answer] |
| [Statement] | Approved decision | [Approval evidence] | — |

Classification rules:

- Use `Confirmed fact` only for statements directly supported by approved evidence.
- Use `Derived interpretation` for consequences or conclusions inferred from confirmed evidence.
- Use `Approved decision` when a stakeholder explicitly confirms a project-level choice.
- Split a statement when one part is confirmed and another part is inferred.
- Use one consistent classification for the same statement throughout the document.

## 4. Background

[Describe the confirmed current situation that led to the project.]

## 5. Problem Statement

[State the observable problem without prescribing a technical solution.]

## 6. Why the Project Is Needed

[Explain why the project should be undertaken and why it matters now, based on evidence.]

## 7. Desired Future Situation

[Describe what should be different after the project succeeds. Label derived interpretations when necessary.]

## 8. Project Goal

[State one clear, evidence-grounded result the project should achieve.]

## 9. Expected Outcomes

- [Expected high-level outcome]

## 10. People Involved

### Intended Users

- [Person or group who will use the software]

### Other People Affected

- [Person or group, or `Not identified in the approved source`]

### Confirmed Responsibilities

- **[Name]:** [Confirmed responsibility and evidence]

If no additional responsibility is confirmed, write:

- `No additional responsibilities identified in the approved source.`

## 11. High-Level Scope

### Included

- [High-level scope item]

### Excluded

- [Explicit exclusion]

### Future Design Considerations

Record future-facing project considerations here only when they do not add capabilities to the current release.

Do not translate a future consideration into architecture or implementation requirements.

- [Future design consideration, classification, and evidence]

## 12. MVP Boundary

The MVP boundary is the smallest useful software scope approved for the first version. It does not include hypotheses, experiments, or business validation.

### Intended User

[Who must be able to use the first version.]

### Minimum Useful Outcome

[What the user must be able to achieve.]

### Included High-Level Capabilities

- [Capability]

### Explicitly Excluded

- [Excluded capability]

### Confirmed Delivery Limits

- [Confirmed deadline, budget, required environment, or other limit]

### Completion Condition

[Observable condition showing that the approved first-version scope has been delivered.]

## 13. Constraints

A constraint is a confirmed condition the project must respect.

- [Confirmed constraint, or `No additional constraints identified in the approved source`]

## 14. Assumptions

An assumption is unconfirmed information temporarily used to continue. Every assumption must have a confirmation path.

- **Assumption:** [Statement]
  - **Why needed:** [Reason]
  - **Confirmation path:** [Person or evidence required]

If none exist, write `No assumptions recorded`.

## 15. Dependencies

A dependency is something outside the project that must be available or completed.

- [Dependency and evidence, or `No dependencies identified in the approved source`]

## 16. Risks and Uncertainties

Separate supported risks from open uncertainties.

- **[Risk or uncertainty]:** [Possible impact]
  - **Classification:** Confirmed fact | Derived interpretation | Open question | Approved decision
  - **Evidence or basis:** [Source or derivation]
  - **Affected project area:** [Scope, schedule, responsibilities, dependency, or other area]

When a risk is derived from a confirmed constraint, classify the risk statement as `Derived interpretation`, while preserving the underlying constraint as a separate `Confirmed fact`.

If none are supported, write `No project-level risks or uncertainties identified in the approved source`.

## 17. Success Criteria

Use observable project-level conditions supported by evidence. Do not add detailed acceptance criteria.

- [Observable success condition]

## 18. Confirmed Decisions and Responsibilities

- **Person who requested the project:** [Name or `Not identified`]
- **Person who makes project-level decisions:** [Name or `Not assigned in the approved source`]
- **Person who confirms the software meets the agreed scope:** [Name or `Not assigned in the approved source`]
- **Person responsible for building the software:** [Name or `Not assigned in the approved source`]

## Working Questions — Remove Before Approval

Include only while clarification is active. Ask the next small round and stop.

### Q1 — [Category]

- **Question:** [Plain-language project-level question]
- **Status:** Open | Answered
- **Answered by:** [Person and role or responsibility]
- **Evidence source:** [Chat answer, meeting note, or source file]
- **Answer:** [Concise answer]
- **Impact:** [What the answer confirms, changes, or excludes]

## 19. Validation Report

Complete before approval. A classification conflict is a blocking validation failure.

- **Approved source modified:** No | Yes — [explain]
- **Unsupported confirmed claims:** 0 | [count and details]
- **Derived interpretations without basis:** 0 | [count and details]
- **Classification conflicts across sections:** 0 | [count and details]
- **Mixed confirmed-and-derived statements:** 0 | [count and details]
- **Stakeholder-confirmed interpretations not promoted:** 0 | [count and details]
- **Assumptions without confirmation path:** 0 | [count and details]
- **Open questions presented as resolved:** 0 | [count and details]
- **Scope contradictions:** 0 | [count and details]
- **Premature downstream detail:** 0 | [count and details]
- **Authorized traceability fields changed:** [rows and fields, or `None`]
- **Unauthorized traceability changes detected:** 0 | [count and details]
- **Traceability Mutation Guard:** Passed | Failed — [details]
- **Working Questions remaining:** 0 | [count]
- **Blocking validation failures:** None | [details]

## 20. Project Context Approval

### Status

- [ ] Ready for Product Requirements
- [ ] Not Ready

### Reviewed by

- **Name:** [Reviewer name]
- **Role or responsibility:** [How this person is authorized]
- **Date:** [YYYY-MM-DD]

### Blocking Issues or Feedback

[List issues or feedback. Write `None` only when `Ready for Product Requirements` is selected.]

### Approval Rule

The document can be closed and passed to `c-manage-product-requirements` only when:

- Exactly one decision is selected.
- `Ready for Product Requirements` is selected.
- Reviewer name, role or responsibility, and date are recorded.
- `Blocking Issues or Feedback` is `None`.

When `Not Ready` is selected, return the document to `Under Clarification`, address the feedback, clear the current approval fields before resubmission, and preserve the prior decision in version control.
