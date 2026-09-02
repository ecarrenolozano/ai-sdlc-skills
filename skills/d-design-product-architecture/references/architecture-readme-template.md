# Architecture

This directory contains the product architecture baseline: the arc42 narrative, canonical Structurizr DSL model, internal-container documentation, and Architecture Decision Records.

**Primary skill:** `d-design-product-architecture`

## Contents

- `architecture.md`: authoritative arc42 architecture narrative and workflow extensions.
- `containers/`: one documentation folder per internal C4 container.
- `diagrams/workspace.dsl`: canonical C4 model.
- `diagrams/docker-compose.yml`: local Structurizr viewer.
- `diagrams/images/`: optional exported SVG or PNG diagrams.
- `adr/`: accepted and historical Architecture Decision Records.

The baseline always includes System Context and Container views. Component, Dynamic, and Deployment views are included only when they materially improve the architecture description.

Do not commit Structurizr runtime files from `diagrams/.structurizr/`. The directory is excluded by `diagrams/.gitignore`.
