# Architecture

This directory contains the product architecture baseline: the arc42 narrative, canonical Structurizr DSL model, internal-container documentation, and Architecture Decision Records.

**Primary skill:** `d-design-product-architecture`

## Contents

- `architecture.md`: authoritative arc42 architecture narrative and workflow extensions.
- `containers/`: one documentation folder per internal C4 container.
- `diagrams/workspace.dsl`: canonical C4 model.
- `diagrams/docker-compose.yml`: local Structurizr viewer.
- `adr/`: accepted and historical Architecture Decision Records.

The current baseline defines a separated Browser Frontend and Flask Backend. It includes System Context, Container, Backend Component, and Deployment views. The Component view exists because the frontend/backend API boundary and backend persistence port are material architecture boundaries.

Do not commit Structurizr runtime files from `diagrams/.structurizr/`. The directory is excluded by `diagrams/.gitignore`.
