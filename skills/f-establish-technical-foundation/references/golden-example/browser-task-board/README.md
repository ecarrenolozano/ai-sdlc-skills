# Browser Task Board Technical Foundation Golden Example

This golden example continues the approved Browser Task Board used by the earlier workflow skills.

## Input

`in-repository/` represents the repository after approved context, requirements, architecture, and repository preparation, but before technical foundation establishment.

## Proposal

`out-proposal.md` shows the visible proposal that must be approved before local writes.

## Output

`out-repository/` demonstrates a minimal foundation pending final human acceptance:

- separate `frontend/` and Python backend source roots;
- Flask application factory and loopback runtime configuration only;
- checkout-based local execution;
- pytest and pytest-bdd configuration;
- unit, integration, regression, and validation test categories;
- technical smoke tests only;
- reproducible developer commands and minimal CI;
- Technical foundation in `Pending Approval`.

The example does not contain task creation, movement, editing, deletion, persistence schema, counters, product API routes, or BDD acceptance scenarios.
