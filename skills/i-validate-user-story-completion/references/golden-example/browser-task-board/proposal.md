# Validation Proposal

## Scope

Validate US-0001 - Create a task.

## Planned BDD Artifacts

- Create `tests/validation/features/create_task.feature`.
- Create `tests/validation/steps/test_create_task_steps.py`.
- Map the approved scenario "Create a task with a title" to one pytest-bdd scenario.

## Commands

```bash
uv run pytest tests/validation/features/create_task.feature -q
uv run pytest tests/validation -q
python3 .agents/skills/i-validate-user-story-completion/scripts/validate_bdd_validation.py . --story US-0001 --require-trace
```

## Traceability

After validation passes, update only the `User story validation` row:

- `Status`: `Complete`
- `Evidence`: passing validation command, feature file, step file, and story mapping
- `Missing or blocked`: `None`
- `Next action`: `Run h-create-implementation-pull-request`

No implementation, issue, PR, or release action is included.
