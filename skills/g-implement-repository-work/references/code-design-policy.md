# Code Design Policy

## Purpose

Translate approved requirements and architecture into developer-owned code design for one selected issue. The code design guides TDD; it does not replace TDD and does not authorize unapproved behavior.

## Architecture Harmony

- Map each planned module, class, function, route handler, interaction, and test to approved C4 containers, components, ADRs, and acceptance criteria.
- Keep frontend code coupled to the backend only through HTTP/JSON contracts.
- Keep backend product logic inside approved backend components.
- Keep persistence behind the approved repository port and adapter boundary.
- Preserve the repository's completed technical foundation unless a separate approval changes it.

## Developer-Owned Decisions

Developers may decide:

- module and package names;
- classes, functions, methods, and route handlers;
- internal DTOs, validation helpers, serializers, and mappers;
- test module placement and fixture shape;
- small interaction sequences inside an approved component boundary.

Developers must route backward when a decision changes:

- approved product behavior or acceptance criteria;
- C4 containers, components, external interfaces, protocols, or deployment;
- persistence technology or data ownership;
- dependencies or repository-wide foundation;
- security, privacy, or operations posture.

## Hybrid Code-Level Architecture

Maintain code-level architecture under `sdlc_docs/02_architecture/` when production work introduces or changes meaningful code structure or contracts.

Use a hybrid structure:

- `sdlc_docs/02_architecture/code-level.md`: central index for cross-container contracts, issue coverage, Structurizr component identifiers, and links to per-container maps.
- `sdlc_docs/02_architecture/containers/<container>/code-level.md`: detailed code map for modules, classes, functions, routes, adapters, schemas, interactions, and tests owned by that C4 container.

Do not store code-level architecture in `sdlc_docs/03_implementation/`; that folder is for backlog priority and implementation coordination.

The code-level documents should include only durable guidance:

- issue and requirement coverage;
- architecture element mapping;
- module and interaction map;
- HTTP/JSON contracts;
- storage adapter shape when relevant;
- test placement rationale.

Do not record temporary TDD notes, command logs, implementation statistics, or speculative future stories.

## Structurizr and Mermaid

Keep Structurizr DSL canonical for C4 system, container, component, and deployment views. Do not expand Structurizr with every file, class, function, route, or DTO.

Use Mermaid inside code-level Markdown when a diagram clarifies implementation design:

- `sequenceDiagram` for runtime interactions across modules, routes, services, adapters, or frontend/backend contracts;
- `flowchart` for decision logic, validation flow, persistence flow, or request handling;
- `classDiagram` for services, ports, adapters, modules, value objects, and their dependencies;
- object/state-style diagrams or small fenced examples for durable payload and state shapes.

Mermaid diagrams must map back to approved C4 containers/components and must not introduce unapproved product behavior or architecture changes.

## TDD Constraint

Code design may identify intended elements, but production behavior still starts with a meaningful failing test. If the design cannot be tested through the selected issue, keep it out of the implementation or mark it as deferred.
