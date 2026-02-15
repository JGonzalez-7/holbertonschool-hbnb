"""Flask application factory for HBnB."""

from __future__ import annotations

from flask import Flask

from app.api import register_api
from app.services import HBnBFacade


def create_app() -> Flask:
    app = Flask(__name__)

    # Configure facade and expose on app extensions for easy access from resources
    app.extensions["facade"] = HBnBFacade()

    # Register API routes
    register_api(app)

    return app


__all__ = ["create_app"]
