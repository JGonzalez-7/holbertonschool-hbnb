"""API registration helper using Flask-RESTX."""

from flask_restx import Api

from .v1 import namespaces


def register_api(app):
    """Attach RESTX Api with v1 namespaces to the Flask app."""

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB REST API",
        prefix="/api/v1",
        doc="/api/docs",
    )

    for ns in namespaces:
        api.add_namespace(ns)

    return api


__all__ = ["register_api"]
