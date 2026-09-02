"""Flask application factory without product routes."""
from __future__ import annotations

from pathlib import Path

from flask import Flask


def create_app() -> Flask:
    """Create the technical Flask application shell."""
    repository_root = Path(__file__).resolve().parents[3]
    frontend_root = repository_root / "frontend"
    return Flask(
        __name__,
        static_folder=str(frontend_root / "static"),
        template_folder=str(frontend_root / "templates"),
    )
