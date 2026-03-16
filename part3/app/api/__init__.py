"""API registration for HBnB Part 3."""

from flask_restx import Api

from .v1 import namespaces


def register_api(app):
    """Attach the REST API to the Flask app."""
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB REST API",
        prefix="/api/v1",
        doc="/api/docs",
    )

    for namespace in namespaces:
        api.add_namespace(namespace)

    return api


__all__ = ["register_api"]
