# Workflow

The repository defines a controlled SDLC workflow for AI-assisted coding agents. Each skill owns a specific stage, set of artifacts, and approval boundary.

## Lifecycle Order

```text
Project request
      |
      v
Clarify project request
      |
      v
Form project context
      |
      v
Manage product requirements
      |
      v
Design product architecture
      |
      v
Synchronize repository requirements
      |
      v
Establish technical foundation
      |
      v
Implement repository work
      |
      v
Validate user story completion
      |
      v
Create implementation pull request
      |
      v
Prepare release and deployment
```

## Control Principles

- Skills preserve original evidence instead of replacing it with summaries.
- Human approval gates are explicit and owned by the relevant stage.
- `sdlc_docs/trace_workflow.md` is the canonical project workflow state when installed in a target repository.
- Later skills consume approved outputs from earlier skills instead of recreating decisions.
- Remote mutations, publishing actions, commits, pull requests, and deployments require separate explicit approval when a skill defines that boundary.

## Generated Skill Pages

The [skill catalog](skills/index.md) is generated from the current `skills/` directory. Each generated page explains one skill's role, process flowchart, resources, validators, examples, and canonical instruction body.
