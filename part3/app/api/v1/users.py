"""User endpoints for HBnB Part 3."""

from __future__ import annotations

from flask import current_app
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from app.models import User

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "id": fields.String(readonly=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "is_admin": fields.Boolean(default=False),
    },
)

user_create_model = api.model(
    "UserCreate",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True, description="Plain password"),
        "is_admin": fields.Boolean(default=False),
    },
)

user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String,
        "last_name": fields.String,
        "email": fields.String,
        "password": fields.String,
        "is_admin": fields.Boolean,
    },
)


def _get_facade():
    facade = current_app.extensions.get("facade") or current_app.config.get("FACADE")
    if facade is None:
        api.abort(500, "Facade not configured on application")
    return facade


@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users without password data."""
        users = _get_facade().list_users()
        return [user.to_dict() for user in users]

    @jwt_required()
    @api.expect(user_create_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a user. Administrator only."""
        if not get_jwt().get("is_admin", False):
            api.abort(403, "Administrator access required")

        payload = api.payload or {}

        try:
            user = _get_facade().create_user(payload)
        except ValueError as exc:
            api.abort(400, str(exc))

        return user.to_dict(), 201


@api.route("/<string:user_id>")
@api.response(404, "User not found")
class UserItem(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id: str):
        """Fetch a single user without password data."""
        user = _get_facade().get_user(user_id)
        if user is None:
            api.abort(404, "User not found")
        return user.to_dict()

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id: str):
        facade = _get_facade()
        user = facade.get_user(user_id)
        if user is None:
            api.abort(404, "User not found")

        payload = api.payload or {}
        is_admin = bool(get_jwt().get("is_admin", False))

        if is_admin:
            invalid_fields = sorted(
                set(payload) - {"first_name", "last_name", "email", "password", "is_admin"}
            )
            if invalid_fields:
                api.abort(400, f"Unsupported field(s): {', '.join(invalid_fields)}")

            if "first_name" in payload:
                if not isinstance(payload["first_name"], str) or not payload["first_name"].strip():
                    api.abort(400, "first_name must be a non-empty string")
                user.first_name = payload["first_name"].strip()

            if "last_name" in payload:
                if not isinstance(payload["last_name"], str) or not payload["last_name"].strip():
                    api.abort(400, "last_name must be a non-empty string")
                user.last_name = payload["last_name"].strip()

            if "email" in payload:
                email = str(payload["email"]).strip().lower()
                if "@" not in email:
                    api.abort(400, "email must contain '@'")
                existing = User.query.filter_by(email=email).first()
                if existing is not None and existing.id != user.id:
                    api.abort(400, "User already exists")
                user.email = email

            if "password" in payload:
                try:
                    user.password = payload["password"]
                except ValueError as exc:
                    api.abort(400, str(exc))

            if "is_admin" in payload:
                if not isinstance(payload["is_admin"], bool):
                    api.abort(400, "is_admin must be a boolean")
                user.is_admin = payload["is_admin"]
        else:
            if get_jwt_identity() != user_id:
                api.abort(403, "You can only modify your own user details")

            invalid_fields = sorted(set(payload) - {"first_name", "last_name"})
            if invalid_fields:
                api.abort(
                    400,
                    f"Unsupported field(s): {', '.join(invalid_fields)}",
                )
        try:
            updated_user = facade.update_user(user_id, payload)
        except ValueError as exc:
            api.abort(400, str(exc))

        if updated_user is None:
            api.abort(404, "User not found")
        return updated_user.to_dict()


__all__ = ["api"]
