"""Review endpoints (v1) using Flask-RESTX."""

from __future__ import annotations

from typing import Any, Dict, List

from flask import current_app
from flask_restx import Namespace, Resource, fields, abort


api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "id": fields.String(readonly=True),
        "rating": fields.Integer(required=True, min=1, max=5),
        "comment": fields.String(required=True),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
    },
)

review_create_model = api.model(
    "ReviewCreate",
    {
        "rating": fields.Integer(required=True, min=1, max=5),
        "comment": fields.String(required=True),
        "user_id": fields.String(required=True),
        "place_id": fields.String(required=True),
    },
)

review_update_model = api.model(
    "ReviewUpdate",
    {
        "rating": fields.Integer(min=1, max=5),
        "comment": fields.String,
    },
)


def _get_facade():
    facade = current_app.extensions.get("facade") or current_app.config.get("FACADE")
    if facade is None:
        abort(500, "Facade not configured on application")
    return facade


@api.route("")
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self) -> List[Dict[str, Any]]:
        """List all reviews."""

        facade = _get_facade()
        return facade.list_reviews()

    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self) -> Dict[str, Any]:
        """Create a review."""

        payload = api.payload or {}
        required = ["rating", "user_id", "place_id"]
        missing = [f for f in required if payload.get(f) is None]
        if missing:
            abort(400, f"Missing required field(s): {', '.join(missing)}")

        rating = payload.get("rating")
        if not (1 <= rating <= 5):
            abort(400, "rating must be between 1 and 5")
        comment = payload.get("comment")
        if comment is None or not str(comment).strip():
            abort(400, "comment must be a non-empty string")

        facade = _get_facade()
        try:
            review = facade.create_review(
                {
                    "rating": rating,
                    "comment": comment,
                    "user_id": payload.get("user_id"),
                    "place_id": payload.get("place_id"),
                }
            )
        except ValueError as exc:
            abort(400, str(exc))
        if review is None:
            abort(404, "User or place not found")
        return review, 201


@api.route("/<string:review_id>")
@api.response(404, "Review not found")
class ReviewItem(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id: str):
        """Retrieve a review."""

        facade = _get_facade()
        review = facade.get_review(review_id)
        if review is None:
            abort(404, "Review not found")
        return review

    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id: str):
        """Update a review."""

        payload = api.payload or {}
        if "rating" in payload:
            rating = payload.get("rating")
            if rating is None or not (1 <= rating <= 5):
                abort(400, "rating must be between 1 and 5")
        if "comment" in payload and (payload.get("comment") is None or not str(payload.get("comment")).strip()):
            abort(400, "comment must be a non-empty string")

        facade = _get_facade()
        try:
            review = facade.update_review(review_id, payload)
        except ValueError as exc:
            abort(400, str(exc))
        if review is None:
            abort(404, "Review not found")
        return review

    @api.response(204, "Deleted")
    def delete(self, review_id: str):
        """Delete a review."""

        facade = _get_facade()
        deleted = facade.delete_review(review_id)
        if not deleted:
            abort(404, "Review not found")
        return "", 204


__all__ = ["api"]
