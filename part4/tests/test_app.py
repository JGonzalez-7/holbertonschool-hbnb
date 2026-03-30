"""Application factory tests for Part 4."""

from __future__ import annotations

from app import create_app
from app.services.backend import BackendClient


def test_create_app_uses_testing_configuration():
    app = create_app("testing")

    assert app.config["TESTING"] is True
    assert app.config["BACKEND_API_URL"] == "http://backend.test/api/v1"
    assert isinstance(app.extensions["backend_client"], BackendClient)

