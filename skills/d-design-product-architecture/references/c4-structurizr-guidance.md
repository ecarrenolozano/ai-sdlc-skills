# C4 and Structurizr Guidance

Official Structurizr sources consulted for this skill:

- https://docs.structurizr.com/dsl/language
- https://docs.structurizr.com/local/quickstart
- https://docs.structurizr.com/ui/diagrams/export

## Canonical Model

Maintain `sdlc_docs/02_architecture/diagrams/workspace.dsl` as the canonical diagram model. Exported images are optional derivatives.

## C4 Mapping to arc42

| arc42 section | C4/Structurizr view |
|---|---|
| 3. Context and Scope | System Context |
| 5. Building Block View | Container and selected Component views |
| 6. Runtime View | selected Dynamic views |
| 7. Deployment View | selected Deployment views |

## Internal Containers

Represent independently running applications and data stores owned by the product as containers. Create exactly one documentation folder for each internal container:

```text
containers/<normalized-container-name>/architecture.md
```

Do not create container folders for people, external software systems, components, deployment nodes, protocols, or libraries.

## Container Detection

A candidate usually qualifies as a container when it has one or more material boundaries involving execution, technology, deployment, interface, data ownership, or processing responsibility. Do not split containers merely to mirror UI pages, use cases, packages, or future speculation.

## Component View Rule

A Component view is required when an ADR or the Architecture Element Register identifies a material internal boundary whose structure is important to the architecture. It is optional otherwise. Defining components in the DSL without a Component view is invalid.

## Diagram Text Quality

- Keep software-system and container descriptions short enough to scan in a diagram. Put detail in Markdown.
- Use intention-level person relationships such as `Uses to manage a personal board` or `Submits analyses`.
- Do not enumerate create, read, update, delete, restore, count, or story-by-story behavior in relationship labels.
- Dynamic-view labels may be more specific because sequence is their purpose.

## View Rules

- Always create stable keys for System Context and Container views.
- Add Component views only when a container needs internal decomposition to answer an architectural question.
- Define every relationship used by a Dynamic view in the model first.
- Scope a Dynamic view to the lowest element that owns all referenced internal elements.
- Define deployment nodes under a deployment environment before creating a Deployment view.
- Use Structurizr deployment view syntax with both the software system and deployment environment before the view key, for example `deployment taskBoard "Browser" "BrowserDeployment" {`.
- Do not duplicate the same view in separate DSL files as coequal sources.

## Viewing with Docker

Generate a Compose file that runs Structurizr locally:

```yaml
services:
  structurizr:
    image: structurizr/structurizr
    command: ["local"]
    ports:
      - "8080:8080"
    volumes:
      - ./:/usr/local/structurizr
```

From the repository root:

```bash
docker compose -f sdlc_docs/02_architecture/diagrams/docker-compose.yml up
```

Open `http://localhost:8080`. Stop it with the corresponding `down` command. Do not automatically run Docker or download images during ordinary skill execution.

## Runtime Files

Create `diagrams/.gitignore` with:

```gitignore
.structurizr/
```

Never include `.structurizr/` indexes, logs, locks, caches, or thumbnails in the architecture package or version control.

## Exported Images

The architect may export PNG or SVG images manually and place them under `diagrams/images/`. Add a Markdown image reference only after verifying the file exists and corresponds to the current view. Prefer SVG when supported.
