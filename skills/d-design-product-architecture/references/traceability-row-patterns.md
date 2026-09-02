# Workflow Traceability Patterns

## Initial Release Rows

```markdown
| Initial requirements | Initial Release | Complete | Product Requirements Management | approved `01_requirements/product_requirements.md` | None | Run d-design-product-architecture |
| Architecture | Initial Release | Not Started | Product Architecture Design | approved requirements available | Architecture baseline has not been created | Run d-design-product-architecture |
| Repository preparation | Initial Release | Not Started | Repository Requirements Synchronization | approved requirements available | Approved architecture missing | Run e-sync-repository-requirements |
```

## Architecture Under Clarification

```markdown
| Architecture | Initial Release | Under Clarification | Product Architecture Design | draft `02_architecture/architecture.md` | Material architecture decisions remain open | Continue d-design-product-architecture |
```

## Architecture Pending Approval

```markdown
| Architecture | Initial Release | Pending Approval | Product Architecture Design | validated `02_architecture/architecture.md`; `02_architecture/diagrams/workspace.dsl` | Human architecture approval required | Review architecture baseline |
```

## Architecture Complete

```markdown
| Architecture | Initial Release | Complete | Product Architecture Design | approved `02_architecture/architecture.md`; validated `02_architecture/diagrams/workspace.dsl` | None | Run e-sync-repository-requirements |
```

Do not reconstruct unrelated rows. A one-time migration may add the Architecture row and update only the exact handoff fields listed in SKILL.md.
