---
name: sdlc-orchestrate-workflow
description: Act as the developer-facing controller for the installed controlled-SDLC skills. Use when the developer asks to start, continue, resume, inspect, or repair a Python project workflow. Locate the repository, bootstrap missing SDLC structure through the bootstrap skill, validate sdlc_docs/trace_workflow.md, select and run the correct owning skill, preserve all approval gates, hide internal skill identifiers during normal guidance, and always explain the immediate objective and next developer action. Do not invent evidence, approvals, completion, or remote state.
---

# SDLC Workflow Orchestration

## Purpose

Guide the developer continuously while keeping workflow ceremony behind the scenes. The developer should not need to know stage identifiers, trace-row mechanics, or routing rules.

## Governing Rules

- Treat `sdlc_docs/trace_workflow.md` as canonical workflow state.
- Preserve every approval boundary defined by the owning stage.
- Never invent evidence, approvals, validation results, issue state, release state, or completion.
- Do not expose exact skill identifiers during normal guidance; use them internally for routing and only show them when diagnosing configuration errors.
- Do not silently repair trace state. Present exact field changes and require explicit approval.
- Re-read relevant state immediately before an approved mutation.
- Allow controlled overlap between `Implementation` and `User story validation` when both are `In Progress` and validation evidence is limited to implemented story subsets.
- Allow controlled overlap between `Implementation` and `Pull request` when the pull request is opened for iterative review and downstream release gating remains inactive.
- Allow controlled overlap between `Implementation` and `Release deployment` when deployment work is limited to approved local release-preparation evidence.

## Control Loop

1. Locate the repository root.
2. If the trace is absent, run the bootstrap workflow and then resume this loop.
3. Run `scripts/validate_workflow_trace.py --require-expected-rows`.
4. If validation reports ambiguity or inconsistency, read `references/workflow-routing-policy.md`, explain the issue in plain language, and propose only permitted repairs.
5. Select the highest-priority gate: blocked information, clarification, human approval, active work, then the first eligible unstarted stage.
6. Route internally to the owning installed skill and follow that skill completely, including its approvals and deterministic validators.
7. Re-run trace validation after any approved workflow mutation.
8. Report: current objective, completed work, evidence, pending approval or blocker, and the next developer action.

## Stage Order

Use this internal order:

```text
sdlc-bootstrap-project (only when structure is absent)
a-clarify-project-request
b-form-project-context
c-manage-product-requirements
d-design-product-architecture
e-sync-repository-requirements
f-establish-technical-foundation
g-implement-repository-work
i-validate-user-story-completion
h-create-implementation-pull-request
j-prepare-release-deployment
```

Allow backward routing only when an owning artifact identifies a material product, architecture, or imported-increment change.

## Controlled Overlap Policy

The orchestrator may keep `Implementation` and `User story validation` active at the same time only when all conditions below are true:

1. `Implementation` is `In Progress`.
2. `User story validation` is `In Progress` for selected implemented stories only.
3. Validation evidence explicitly names story subset and executed commands.
4. `Pull request` and `Release deployment` rows remain downstream and are not activated early.

If these conditions are not met, route to repair or to the owning stage before continuing.

The orchestrator may also keep `Implementation` and `Pull request` active at the same time only when all conditions below are true:

1. `Implementation` is `In Progress`.
2. `Pull request` is `In Progress` with explicit draft-or-review evidence.
3. Remaining implementation or validation scope is explicitly tracked in trace blockers.
4. `Release deployment` remains `Not Started`.

If these conditions are not met, keep the pull request row downstream and non-active.

The orchestrator may also keep `Implementation` and `Release deployment` active at the same time only when all conditions below are true:

1. `Implementation` is `In Progress`.
2. `Release deployment` is `In Progress` for approved local preparation or smoke-deployment evidence.
3. Deployment work does not publish artifacts, tags, or remote releases without separate explicit approval.
4. Remaining implementation and validation gaps stay explicitly tracked.

If these conditions are not met, keep release deployment downstream and non-active.

The orchestrator may also keep `Implementation`, `Pull request`, and `Release deployment` active at the same time only when all conditions below are true:

1. `Implementation` is `In Progress`.
2. `Pull request` is `In Progress` for iterative review of approved local work.
3. `Release deployment` is `In Progress` for approved local preparation or smoke-deployment evidence.
4. No remote publishing, tagging, artifact release, or external deployment occurs without separate explicit approval.

If these conditions are not met, keep release deployment downstream and non-active.

## Repair Boundary

After explicit approval, repair only missing standard rows, obsolete internal identifiers, unsupported downstream handoff states with no evidence, or blocker wording already proven by an owning artifact. Never mark another stage complete, create approval evidence, rewrite history, or mutate GitHub, version control, release, or deployment state.

## Progressive Resources

- Read `references/workflow-routing-policy.md` only for ambiguous routing or trace repair.
- Read `references/golden-example/README.md` only when a concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
- Run `scripts/validate_workflow_trace.py` for every trace assessment.
