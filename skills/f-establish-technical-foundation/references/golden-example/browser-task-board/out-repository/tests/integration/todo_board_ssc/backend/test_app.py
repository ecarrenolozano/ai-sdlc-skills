"""
Integration tests for the Flask application factory.

Test organization:
    - Nominal Case Tests
"""

# Standard library imports
from pathlib import Path

# Third-party imports
import pytest
from flask import Flask

# Local application imports
from todo_board_ssc.backend import create_app

pytestmark = pytest.mark.integration


# =============================================================================
# ==== Class Test Cases
# =============================================================================


class TestApplicationFactory:
    """Tests for the technical Flask application shell."""

    # ---- Nominal Case Tests

    def test_create_app_returns_flask_application(self) -> None:
        """The approved factory creates a Flask application."""
        assert isinstance(create_app(), Flask)

    def test_frontend_roots_are_outside_backend_package(self) -> None:
        """Frontend static and template roots remain separate from backend source."""
        app = create_app()

        assert app.static_folder is not None
        assert app.template_folder is not None
        assert Path(app.static_folder).parts[-2:] == ("frontend", "static")
        assert Path(app.template_folder).parts[-2:] == ("frontend", "templates")
