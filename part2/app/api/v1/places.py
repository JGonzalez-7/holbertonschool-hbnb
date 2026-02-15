"""Place endpoints (v1) using Flask-RESTX.

Supports listing with filters, creation, retrieval, update, and delete. Business
rules and data shaping are delegated to the facade configured on the Flask
application (`app.extensions["facade"]` or `app.config["FACADE"]`).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from flask import current_app
from flask_restx import Namespace, Resource, fields, reqparse, abort


api = Namespace("places", description="Place operations")

amenity_summary = api.model(
    "AmenitySummary",
    {
        "id": fields.String,
        "name": fields.String,
    },
)

owner_summary = api.model(
    "OwnerSummary",
    {
        "id": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "email": fields.String,
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
        "owner_id": fields.String(required=True, description="Owner user id"),
        "owner": fields.Nested(owner_summary, description="Owner details"),
        "amenities": fields.List(fields.Nested(amenity_summary)),
        "reviews": fields.List(
            fields.Nested(
                api.model(
                    "ReviewSummary",
                    {
                        "id": fields.String,
                        "rating": fields.Integer,
                        "comment": fields.String,
                        "user_id": fields.String,
                    },
                )
            ),
            description="Reviews for this place",
        ),
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
        "owner_id": fields.String(required=True),
        "amenity_ids": fields.List(fields.String, description="IDs of amenities"),
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
        "amenity_ids": fields.List(fields.String, description="IDs of amenities"),
    },
)


list_parser = api.parser()
list_parser.add_argument("min_price", type=float, required=False, location="args")
list_parser.add_argument("max_price", type=float, required=False, location="args")
list_parser.add_argument("lat", type=float, required=False, location="args")
list_parser.add_argument("lng", type=float, required=False, location="args")
list_parser.add_argument("radius", type=float, required=False, location="args")
list_parser.add_argument(
    "amenity_id", type=str, action="append", required=False, location="args"
)


def _get_facade():
    """Retrieve the configured facade instance."""

    facade = current_app.extensions.get("facade") or current_app.config.get("FACADE")
    if facade is None:
        abort(500, "Facade not configured on application")
    return facade


@api.route("")
class PlaceList(Resource):
    @api.expect(list_parser)
    @api.marshal_list_with(place_model)
    def get(self) -> List[Dict[str, Any]]:
        """List places with optional filters."""

        args = list_parser.parse_args()
        filters = {
            key: value
            for key, value in args.items()
            if value is not None and key != "amenity_id"
        }
        # Allow multiple amenity_id query params -> list
        if args.get("amenity_id"):
            filters["amenity_ids"] = args.get("amenity_id")

        facade = _get_facade()
        return facade.list_places(filters)

    @api.expect(place_create_model, validate=True)
    @api.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place."""

        payload = api.payload or {}
        required_fields = ["name", "price", "latitude", "longitude", "owner_id"]
        missing = [f for f in required_fields if not payload.get(f)]
        if missing:
            abort(400, f"Missing required field(s): {', '.join(missing)}")

        place_data: Dict[str, Any] = {
            "name": payload.get("name"),
            "description": payload.get("description"),
            "price": payload.get("price"),
            "latitude": payload.get("latitude"),
            "longitude": payload.get("longitude"),
            "owner_id": payload.get("owner_id"),
            "amenity_ids": payload.get("amenity_ids") or [],
        }

        facade = _get_facade()
        try:
            result = facade.create_place(place_data)
        except ValueError as exc:
            abort(400, str(exc))
        if result is None:
            # Facade should raise/handle, but guard for safety
            abort(404, "Owner or amenities not found")
        return result, 201


@api.route("/<string:place_id>")
@api.response(404, "Place not found")
class PlaceItem(Resource):
    @api.marshal_with(place_model)
    def get(self, place_id: str):
        """Retrieve a single place."""

        facade = _get_facade()
        place = facade.get_place(place_id)
        if place is None:
            abort(404, "Place not found")
        return place

    @api.expect(place_update_model, validate=True)
    @api.marshal_with(place_model)
    def put(self, place_id: str):
        """Update a place."""

        payload = api.payload or {}
        facade = _get_facade()
        try:
            place = facade.update_place(place_id, payload)
        except ValueError as exc:
            abort(400, str(exc))
        if place is None:
            abort(404, "Place not found")
        return place


__all__ = ["api"]
