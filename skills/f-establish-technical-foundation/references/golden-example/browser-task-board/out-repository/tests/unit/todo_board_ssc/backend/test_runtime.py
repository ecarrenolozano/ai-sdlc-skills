"""
Unit tests for local runtime settings.

Test organization:
    - Nominal Case Tests
"""

# Standard library imports
import ipaddress

# Third-party imports
import pytest

# Local application imports
from todo_board_ssc.backend.runtime import DEFAULT_HOST

pytestmark = pytest.mark.unit


# =============================================================================
# ==== Class Test Cases
# =============================================================================


class TestRuntimeSettings:
    """Tests for approved local runtime settings."""

    # ---- Nominal Case Tests

    def test_default_host_is_loopback(self) -> None:
        """The default backend host is the approved IPv4 loopback address."""
        assert ipaddress.ip_address(DEFAULT_HOST).is_loopback
