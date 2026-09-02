# Validation Execution

## Commands

```bash
uv run pytest tests/validation/features/create_task.feature -q
```

Result: passed.

```bash
uv run pytest tests/validation -q
```

Result: passed.

```bash
python3 .agents/skills/i-validate-user-story-completion/scripts/validate_bdd_validation.py . --story US-0001 --require-trace
```

Result: passed.

## Evidence

- Feature file: `tests/validation/features/create_task.feature`
- Step file: `tests/validation/steps/test_create_task_steps.py`
- Story mapping: US-0001 criterion mapped to one scenario
- Trace update: `User story validation` row complete
