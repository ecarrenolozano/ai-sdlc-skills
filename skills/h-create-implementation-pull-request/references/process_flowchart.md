# Process Flowchart

```mermaid
flowchart TD
    A[Inspect required inputs] --> B[Validate preconditions]
    B --> C[Prepare proposal or perform read-only analysis]
    C --> D{Approval required?}
    D -- Yes --> E[Obtain explicit approval]
    D -- No --> F[Execute permitted work]
    E --> F
    F --> G[Run deterministic validation]
    G --> H[Record evidence and hand off]
```

This audit view summarizes `h-create-implementation-pull-request`. The skill entrypoint and validators remain authoritative.
