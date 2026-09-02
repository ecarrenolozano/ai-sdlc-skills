"""pytest-bdd binding module for <feature>."""

# Standard library imports

# Third-party imports
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

# Local application imports


pytestmark = pytest.mark.validation

scenarios("<feature-file>.feature")


# =============================================================================
# ==== Fixtures and Setup
# =============================================================================


@pytest.fixture
def scenario_context() -> dict[str, object]:
    """Return isolated mutable state for one scenario."""
    return {}


# =============================================================================
# ==== Given Steps
# =============================================================================


@given(parsers.parse("<approved initial context>"))
def approved_initial_context(scenario_context: dict[str, object]) -> None:
    """Establish the approved initial state."""
    raise NotImplementedError


# =============================================================================
# ==== When Steps
# =============================================================================


@when(parsers.parse("<approved user action>"))
def approved_user_action(scenario_context: dict[str, object]) -> None:
    """Perform the approved action."""
    raise NotImplementedError


# =============================================================================
# ==== Then Steps
# =============================================================================


@then(parsers.parse("<approved observable result>"))
def approved_observable_result(scenario_context: dict[str, object]) -> None:
    """Verify the approved observable result."""
    raise NotImplementedError
