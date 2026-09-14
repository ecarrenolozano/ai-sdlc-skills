# Installation

The canonical project-level installation location is:

```text
.agents/skills/
```

Generated projects can install or update this repository's skills into that location while recording the exact version used.

## Versioning

This repository follows Semantic Versioning. Projects should record the installed version so that AI-assisted SDLC behavior remains reproducible.

## Updating

The long-term update interface described by the repository is:

```bash
ai-sdlc skills status
ai-sdlc skills update
```

An updater should detect locally modified skills and avoid overwriting them silently.
