"""BDD validation steps for creating a task."""

from pytest_bdd import given, scenario, then, when


@scenario("create_task.feature", "US-0001 - Create a task with a title")
def test_create_task_with_title() -> None:
    """Validate the approved create-task story."""


@given("the board is available", target_fixture="board")
def board_available() -> dict[str, list[dict[str, str]]]:
    return {"TODO": []}


@when("the user creates a task with a non-empty title")
def create_task(board: dict[str, list[dict[str, str]]]) -> None:
    board["TODO"].append({"title": "Write release notes"})


@then("the task is added to TODO with that title")
def task_added_to_todo(board: dict[str, list[dict[str, str]]]) -> None:
    assert board["TODO"] == [{"title": "Write release notes"}]
