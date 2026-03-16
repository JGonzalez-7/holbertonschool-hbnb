"""Application factory and shared Flask extensions for HBnB Part 3."""

from __future__ import annotations

from pathlib import Path

from config import config as config_map
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def _resolve_config(config_object: str | type | None) -> str | type:
    """Return a Flask-compatible configuration object."""
    if config_object is None:
        return config_map["default"]

    if isinstance(config_object, str):
        return config_map.get(config_object, config_object)

    return config_object


def create_app(config_object: str | type | None = None) -> Flask:
    """Create and configure the Flask application instance."""
    from app.api import register_api
    from app.services import HBnBFacade

    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_object(_resolve_config(config_object))
    app.url_map.strict_slashes = False

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    app.extensions["facade"] = HBnBFacade()
    register_api(app)

    with app.app_context():
        db.create_all()

    return app


__all__ = ["bcrypt", "create_app", "db", "jwt"]
