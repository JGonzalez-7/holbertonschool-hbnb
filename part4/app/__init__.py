"""Application factory for the HBnB Part 4 web client."""

from __future__ import annotations

from pathlib import Path

from flask import Flask

from config import config as config_map


def _resolve_config(config_object: str | type | None) -> str | type:
    """Return a Flask-compatible configuration object."""
    if config_object is None:
        return config_map["default"]

    if isinstance(config_object, str):
        return config_map.get(config_object, config_object)

    return config_object


def create_app(config_object: str | type | None = None) -> Flask:
    """Create and configure the Flask application."""
    from app.routes.api import api_bp
    from app.routes.web import web_bp
    from app.services.backend import BackendClient

    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_object(_resolve_config(config_object))
    app.url_map.strict_slashes = False

    app.extensions["backend_client"] = BackendClient(
        base_url=app.config["BACKEND_API_URL"],
        timeout=float(app.config["BACKEND_TIMEOUT"]),
    )

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    return app


__all__ = ["create_app"]

