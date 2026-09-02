# AI SDLC Skills

Reusable AI agent skills for guiding Python projects through a structured software development lifecycle.

This repository contains the canonical collection of skills used by the `ai-assisted-python-template` project. The skills are designed to support developers and research software engineers through requirements, architecture, implementation, testing, validation, and deployment.

## Purpose

The goal of this repository is to separate the AI-assisted SDLC workflow from the Cookiecutter template itself.

The Cookiecutter template is responsible for creating a new Python project, while this repository is responsible for maintaining and distributing the skills used by AI agents during the software development lifecycle.

This separation allows existing projects to update their skills without regenerating the project or manually copying files from a newer version of the template.

## Repository structure

```text
ai-sdlc-skills/
├── CHANGELOG.md
├── LICENSE
├── README.md
└── skills/
    ├── a-clarify-project-request/
    ├── b-form-project-context/
    ├── c-manage-product-requirements/
    ├── d-design-product-architecture/
    ├── ...
    └── sdlc-orchestrate-workflow/
```

Each directory under `skills/` contains one reusable agent skill.

A skill typically contains a `SKILL.md` entry point and may also contain supporting scripts, references, templates, or other resources required by the workflow.

## Workflow

The skills belong to a common software development workflow and are intended to be used together.

A typical flow is:

```text
Project request
      ↓
Clarify requirements
      ↓
Build project context
      ↓
Define product requirements
      ↓
Design architecture
      ↓
Prepare implementation
      ↓
Implement features
      ↓
Test and validate
      ↓
Prepare release and deployment
```

The exact workflow is coordinated by the orchestration skills included in this repository.

## Installation location

The canonical project-level installation location is:

```text
.agents/skills/
```

Using `.agents/skills` provides a provider-neutral location for skills and improves portability between compatible AI coding agents.

Some providers may require or support additional provider-specific locations. Those mappings should be handled by the project tooling rather than by modifying the skills themselves.

## Versioning

This repository follows Semantic Versioning.

For example:

```text
v1.0.0
v1.1.0
v1.2.0
v2.0.0
```

Projects using these skills should record the exact installed version so that the development workflow remains reproducible.

Minor and patch releases should remain backward compatible whenever possible.

Major releases may introduce changes to workflow structure, artifacts, conventions, or expected project layout.

See [CHANGELOG.md](CHANGELOG.md) for release details.

## Updating skills

The long-term goal is to allow generated projects to manage the skills as a versioned dependency.

The intended interface is:

```bash
ai-sdlc skills status
```

to inspect the installed and available versions, and:

```bash
ai-sdlc skills update
```

to safely update the local skills.

The updater should detect locally modified skills and avoid overwriting them silently.

## Relationship with the Cookiecutter template

This repository contains the skills.

The project template is maintained separately in:

```text
ai-assisted-python-template
```

The responsibilities are intentionally separated:

```text
ai-assisted-python-template
        │
        │ creates
        ▼
   Python project
        │
        │ installs / updates
        ▼
   ai-sdlc-skills
```

The Cookiecutter template should therefore not be considered the canonical source of skill definitions.

## Compatibility

The skills are designed to use the open `SKILL.md` convention and to remain as portable as possible across AI coding agents.

The canonical representation should remain provider-neutral. Provider-specific installation behavior should be implemented by installation or update tooling.

## Contributing

Contributions to improve the workflow, documentation, validation rules, or individual skills are welcome.

When modifying a skill, consider the impact on the complete SDLC workflow because skills may depend on artifacts or conventions established by earlier stages.

Significant workflow changes should be documented in `CHANGELOG.md`.

## License

This project is distributed under the terms defined in the [LICENSE](LICENSE) file.
