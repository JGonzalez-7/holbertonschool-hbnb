"""Place endpoints for HBnB Part 3."""

from __future__ import annotations

from flask import current_app
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.models import Place

api = Namespace("places", description="Place operations")

owner_summary = api.model(
    "PlaceOwnerSummary",
    {
        "id": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "email": fields.String,
        "is_admin": fields.Boolean,
    },
)

review_summary = api.model(
    "PlaceReviewSummary",
    {
        "id": fields.String,
        "rating": fields.Integer,
        "comment": fields.String,
        "user_id": fields.String,
        "place_id": fields.String,
    },
)

amenity_summary = api.model(
    "PlaceAmenitySummary",
    {
        "id": fields.String,
        "name": fields.String,
    },
)

place_model = api.model(
    "Place",
    {
        "id": fields.String(readonly=True),
        "name": fields.String(required=True),
        "description": fields.String,
        "price": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "owner_id": fields.String(required=True),
        "owner": fields.Nested(owner_summary),
        "reviews": fields.List(fields.Nested(review_summary)),
        "amenities": fields.List(fields.Nested(amenity_summary)),
        "average_rating": fields.Float,
    },
)

place_create_model = api.model(
    "PlaceCreate",
    {
        "name": fields.String(required=True),
        "description": fields.String,
        "price": fields.Float(required=True),
        "latitude": fields.Float(required=True),
        "longitude": fields.Float(required=True),
        "owner_id": fields.String,
        "amenity_ids": fields.List(fields.String),
    },
)

place_update_model = api.model(
    "PlaceUpdate",
    {
        "name": fields.String,
        "description": fields.String,
        "price": fields.Float,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "amenity_ids": fields.List(fields.String),
    },
)


def _get_facade():
    facade = current_app.extensions.get("facade") or current_app.config.get("FACADE")
    if facade is None:
        api.abort(500, "Facade not configured on application")
    return facade


def _get_place_or_404(place_id: str) -> Place:
    place = _get_facade().get_place(place_id)
    if place is None:
        api.abort(404, "Place not found")
    return place


@api.route("/")
class PlaceList(Resource):
    @api.marshal_list_with(place_model)
    def get(self):
        """List places. Public endpoint."""
        facade = _get_facade()
        return [facade.serialize_place(place) for place in facade.list_places()]

    @jwt_required()
    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a place owned by the authenticated user."""
        payload = api.payload or {}

        try:
            Place.validate_payload(payload)
        except ValueError as exc:
            api.abort(400, str(exc))

        is_admin = bool(get_jwt().get("is_admin", False))
        owner_id = payload.get("owner_id") if is_admin else get_jwt_identity()
        if owner_id is None:
            owner_id = get_jwt_identity()
        if not is_admin and owner_id != get_jwt_identity():
            api.abort(403, "You can only create places for yourself")
        try:
            place = _get_facade().create_place({**payload, "owner_id": owner_id})
        except ValueError as exc:
            if str(exc) == "Owner not found":
                api.abort(404, str(exc))
            api.abort(400, str(exc))
        return _get_facade().serialize_place(place), 201


@api.route("/<string:place_id>")
@api.response(404, "Place not found")
class PlaceItem(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id: str):
        """Fetch a single place. Public endpoint."""
        return _get_facade().serialize_place(_get_place_or_404(place_id))

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.marshal_with(place_model)
    def put(self, place_id: str):
        """Update a place if the authenticated user owns it."""
        place = _get_place_or_404(place_id)
        if place.owner_id != get_jwt_identity() and not get_jwt().get("is_admin", False):
            api.abort(403, "You can only modify your own places")

        try:
            updated_place = _get_facade().update_place(place_id, api.payload or {})
        except ValueError as exc:
            api.abort(400, str(exc))

        if updated_place is None:
            api.abort(404, "Place not found")
        return _get_facade().serialize_place(updated_place)

    @jwt_required()
    @api.response(204, "Deleted")
    def delete(self, place_id: str):
        """Delete a place if the authenticated user owns it."""
        place = _get_place_or_404(place_id)
        if place.owner_id != get_jwt_identity() and not get_jwt().get("is_admin", False):
            api.abort(403, "You can only modify your own places")

        _get_facade().delete_place(place_id)
        return "", 204


__all__ = ["api"]
