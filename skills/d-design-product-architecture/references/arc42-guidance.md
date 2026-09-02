# arc42 Guidance

Use the official arc42 template as the normative structure for the root architecture narrative.

Official sources consulted for this skill:

- https://arc42.org/overview
- https://docs.arc42.org/section-1/
- https://docs.arc42.org/section-2/
- https://docs.arc42.org/section-3/
- https://docs.arc42.org/section-4/
- https://docs.arc42.org/section-5/
- https://docs.arc42.org/section-6/
- https://docs.arc42.org/section-7/
- https://docs.arc42.org/section-8/
- https://docs.arc42.org/section-9/
- https://docs.arc42.org/section-10/
- https://docs.arc42.org/section-11/
- https://docs.arc42.org/section-12/

## Required Root Section Order

1. Introduction and Goals
2. Constraints
3. Context and Scope
4. Solution Strategy
5. Building Block View
6. Runtime View
7. Deployment View
8. Crosscutting Concepts
9. Architectural Decisions
10. Quality Requirements
11. Risks and Technical Debt
12. Glossary

Do not rename, merge, remove, or reorder these root sections.

## Tailoring Rule

arc42 is tailorable. Preserve the root headings while adjusting depth to system size and risk. A section may state that no additional detail is required, but it must explain why. Never use an empty heading or a bare `TBD`, `TODO`, `N/A`, or `To be defined` in a baseline submitted for approval.

## Recommended Subsections

```text
1.1 Requirements Overview
1.2 Quality Goals
1.3 Stakeholders

2.1 Technical Constraints
2.2 Organizational Constraints
2.3 Conventions

3.1 Business Context
3.2 Technical Context

5.1 Whitebox Overall System
5.2 Level 2
5.3 Level 3

7.1 Infrastructure Level 1
7.2 Infrastructure Level 2

10.1 Quality Requirements Overview
10.2 Quality Scenarios
```

Subsections may be omitted when they add no value, except that 1.1, 1.2, 1.3, 3.1, 5.1, 10.1, and 10.2 should normally be present in an initial baseline.

## Product Behavior Boundary

Architecture explains structure and technical responsibilities; it does not silently expand product behavior.

- User-visible behavior must trace to approved Product Requirements.
- Architect decisions may define internal boundaries, containers, persistence ownership, deployment, protocols, and technical constraints.
- A product-facing proposal that changes what users can do, see, or expect must return to Product Requirements.
- Do not hide such proposals in Crosscutting Concepts, quality scenarios, risk mitigations, diagram labels, or container responsibilities.
- A Pending Approval or Complete baseline must not contain `Proposed` product-facing behavior.

## Section Intent

### 1. Introduction and Goals

Keep the requirement overview short and link to Product Requirements. Record the top three to five architecture quality goals and the stakeholders who need, use, approve, or maintain the architecture.

### 2. Constraints

Record facts that limit design or implementation choices. Separate confirmed requirements, architect decisions, internal architecture constraints, and open decisions.

### 3. Context and Scope

Delimit the system from users and external systems. Explain business inputs and outputs. Add technical channels and protocols only when known and relevant. Reference the Structurizr System Context view.

### 4. Solution Strategy

Summarize fundamental structural ideas, major technology choices, decomposition, and approaches used to satisfy top quality goals. Link significant choices to ADRs.

### 5. Building Block View

Describe the static hierarchy as white boxes containing black boxes. The overall system whitebox should correspond to the C4 Container view. Add deeper levels selectively. When a material ADR depends on an internal boundary, document it in Level 2 and a Component view.

### 6. Runtime View

Explain important successful, failure, recovery, operational, or administrative scenarios. Use Dynamic views only when sequence adds value.

### 7. Deployment View

Describe infrastructure and mapping of software building blocks to it. Explain when no separate infrastructure is required.

### 8. Crosscutting Concepts

Document recurring technical approaches that affect multiple building blocks. Use the required classification and evidence table. Do not introduce unapproved user-visible behavior here.

### 9. Architectural Decisions

Summarize consequential decisions and link their ADRs. Do not duplicate the full ADR content.

### 10. Quality Requirements

Provide an overview of quality requirements and concrete scenarios. Do not invent measurable thresholds or user-facing guarantees that were not agreed.

### 11. Risks and Technical Debt

Distinguish risks, accepted debt, and unresolved uncertainty. Include impact, mitigation, owner or next action, and status when available. A mitigation must not silently become a new product requirement.

### 12. Glossary

Define only terms needed to understand the architecture. Do not copy an unrelated complete project glossary.
