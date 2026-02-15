"""Amenity endpoints (v1) using Flask-RESTX.

Endpoints cover basic CRUD operations and delegate business rules to the
facade. The facade instance is expected to be attached to the Flask app (e.g.
`app.config["FACADE"]` or `app.extensions["facade"]`).
"""

from __future__ import annotations

from typing import Any, Dict, List

from flask import current_app
from flask_restx import Namespace, Resource, fields, abort


api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "id": fields.String(readonly=True, description="Amenity identifier"),
        "name": fields.String(required=True, description="Amenity name"),
    },
)

amenity_create_model = api.model(
    "AmenityCreate",
    {"name": fields.String(required=True, description="Amenity name")},
)


def _get_facade():
    """Retrieve the facade instance configured on the Flask app."""

    facade = current_app.extensions.get("facade") or current_app.config.get("FACADE")
    if facade is None:
        abort(500, "Facade not configured on application")
    return facade


@api.route("")  
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self) -> List[Dict[str, Any]]:
        """List all amenities."""

        facade = _get_facade()
        return facade.list_amenities()

    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self) -> Dict[str, Any]:
        """Create a new amenity."""

        payload = api.payload or {}
        name = (payload.get("name") or "").strip()
        if not name:
            abort(400, "name is required")

        facade = _get_facade()
        try:
            return facade.create_amenity({"name": name}), 201
        except ValueError as exc:
            abort(400, str(exc))


@api.route("/<string:amenity_id>")
@api.response(404, "Amenity not found")
class AmenityItem(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id: str) -> Dict[str, Any]:
        """Retrieve a single amenity."""

        facade = _get_facade()
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            abort(404, "Amenity not found")
        return amenity

    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id: str) -> Dict[str, Any]:
        """Update amenity name."""

        payload = api.payload or {}
        name = (payload.get("name") or "").strip()
        if not name:
            abort(400, "name is required")

        facade = _get_facade()
        try:
            amenity = facade.update_amenity(amenity_id, {"name": name})
        except ValueError as exc:
            abort(400, str(exc))
        if amenity is None:
            abort(404, "Amenity not found")
        return amenity


__all__ = ["api"]
