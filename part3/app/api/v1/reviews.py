"""Review endpoints for HBnB Part 3."""

from __future__ import annotations

from flask import current_app
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.models import Review

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
        "place_id": fields.String(required=True),
        "user_id": fields.String,
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
        api.abort(500, "Facade not configured on application")
    return facade


def _get_review_or_404(review_id: str) -> Review:
    review = _get_facade().get_review(review_id)
    if review is None:
        api.abort(404, "Review not found")
    return review


@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_model)
    def get(self):
        """List reviews. Public endpoint."""
        return [review.to_dict() for review in _get_facade().list_reviews()]

    @jwt_required()
    @api.expect(review_create_model, validate=True)
    @api.marshal_with(review_model, code=201)
    def post(self):
        """Create a review for a place the user does not own and has not reviewed."""
        payload = api.payload or {}

        try:
            Review.validate_payload(payload)
        except ValueError as exc:
            api.abort(400, str(exc))

        facade = _get_facade()
        place = facade.get_place(str(payload["place_id"]))
        if place is None:
            api.abort(404, "Place not found")

        is_admin = bool(get_jwt().get("is_admin", False))
        current_user_id = payload.get("user_id") if is_admin else get_jwt_identity()
        if current_user_id is None:
            current_user_id = get_jwt_identity()
        if not is_admin and current_user_id != get_jwt_identity():
            api.abort(403, "You can only create reviews for yourself")
        if facade.get_user(str(current_user_id)) is None:
            api.abort(404, "User not found")

        if place.owner_id == current_user_id and not is_admin:
            api.abort(400, "You cannot review your own place")

        existing_review = facade.get_review_by_user_and_place(str(current_user_id), place.id)
        if existing_review is not None:
            api.abort(400, "You have already reviewed this place")

        try:
            review = facade.create_review(
                {
                    "rating": int(payload["rating"]),
                    "comment": payload["comment"].strip(),
                    "user_id": str(current_user_id),
                    "place_id": place.id,
                }
            )
        except ValueError as exc:
            api.abort(400, str(exc))
        return review.to_dict(), 201


@api.route("/<string:review_id>")
@api.response(404, "Review not found")
class ReviewItem(Resource):
    @api.marshal_with(review_model)
    def get(self, review_id: str):
        """Fetch a single review. Public endpoint."""
        return _get_review_or_404(review_id).to_dict()

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_model)
    def put(self, review_id: str):
        """Update a review if the authenticated user authored it."""
        review = _get_review_or_404(review_id)
        if review.user_id != get_jwt_identity() and not get_jwt().get("is_admin", False):
            api.abort(403, "You can only modify your own reviews")

        try:
            updated_review = _get_facade().update_review(review_id, api.payload or {})
        except ValueError as exc:
            api.abort(400, str(exc))

        if updated_review is None:
            api.abort(404, "Review not found")
        return updated_review.to_dict()

    @jwt_required()
    @api.response(204, "Deleted")
    def delete(self, review_id: str):
        """Delete a review if the authenticated user authored it."""
        review = _get_review_or_404(review_id)
        if review.user_id != get_jwt_identity() and not get_jwt().get("is_admin", False):
            api.abort(403, "You can only modify your own reviews")

        _get_facade().delete_review(review_id)
        return "", 204


__all__ = ["api"]
