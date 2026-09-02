# Blocked Gate Examples

## Missing Approval

Row: `Architecture`

Status: `Pending Approval`

Recommendation: obtain human architecture approval. Do not run `e-sync-repository-requirements` yet.

## Missing Validation

Row: `Pull request`

Status: `Not Started`

Blocker: BDD validation row is missing or not complete.

Recommendation: run `i-validate-user-story-completion`.

## Unclear Deployment Target

Row: `Release deployment`

Status: `Under Clarification`

Blocker: deployment target and operations responsibility are not approved.

Recommendation: route the missing decision to requirements or architecture before release/deployment preparation continues.
