"""Amenity endpoints for HBnB Part 3."""

from __future__ import annotations

from flask import current_app
from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "id": fields.String(readonly=True),
        "name": fields.String(required=True),
    },
)

amenity_create_model = api.model(
    "AmenityCreate",
    {"name": fields.String(required=True)},
)


def _require_admin() -> None:
    if not get_jwt().get("is_admin", False):
        api.abort(403, "Administrator access required")


def _get_facade():
    facade = current_app.extensions.get("facade") or current_app.config.get("FACADE")
    if facade is None:
        api.abort(500, "Facade not configured on application")
    return facade


def _get_amenity_or_404(amenity_id: str):
    amenity = _get_facade().get_amenity(amenity_id)
    if amenity is None:
        api.abort(404, "Amenity not found")
    return amenity


@api.route("/")
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        """List amenities. Public endpoint."""
        return [amenity.to_dict() for amenity in _get_facade().list_amenities()]

    @jwt_required()
    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create an amenity. Administrator only."""
        _require_admin()

        try:
            amenity = _get_facade().create_amenity(api.payload or {})
        except ValueError as exc:
            api.abort(400, str(exc))

        return amenity.to_dict(), 201


@api.route("/<string:amenity_id>")
@api.response(404, "Amenity not found")
class AmenityItem(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id: str):
        """Fetch a single amenity. Public endpoint."""
        return _get_amenity_or_404(amenity_id).to_dict()

    @jwt_required()
    @api.expect(amenity_create_model, validate=True)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id: str):
        """Update an amenity. Administrator only."""
        _require_admin()
        _get_amenity_or_404(amenity_id)

        try:
            amenity = _get_facade().update_amenity(amenity_id, api.payload or {})
        except ValueError as exc:
            api.abort(400, str(exc))

        if amenity is None:
            api.abort(404, "Amenity not found")
        return amenity.to_dict()


__all__ = ["api"]
