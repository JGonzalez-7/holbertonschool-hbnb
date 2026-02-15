"\"\"\"User endpoints (v1) using Flask-RESTX.\"\"\""

from __future__ import annotations

from typing import Any, Dict, List

from flask import current_app
from flask_restx import Namespace, Resource, fields, abort


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
        abort(500, "Facade not configured on application")
    return facade


@api.route("")
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self) -> List[Dict[str, Any]]:
        """List users."""

        facade = _get_facade()
        return facade.list_users()

    @api.expect(user_create_model, validate=True)
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a user."""

        payload = api.payload or {}
        required = ["first_name", "last_name", "email", "password"]
        missing = [f for f in required if not payload.get(f)]
        if missing:
            abort(400, f"Missing required field(s): {', '.join(missing)}")

        facade = _get_facade()
        try:
            user = facade.register_user(
                {
                    "first_name": payload["first_name"],
                    "last_name": payload["last_name"],
                    "email": payload["email"],
                    "password": payload["password"],
                    "is_admin": payload.get("is_admin", False),
                }
            )
        except ValueError as exc:
            abort(400, str(exc))
        if user is None:
            abort(400, "User already exists")
        return user, 201


@api.route("/<string:user_id>")
@api.response(404, "User not found")
class UserItem(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id: str):
        """Retrieve a user."""

        facade = _get_facade()
        user = facade.get_user(user_id)
        if user is None:
            abort(404, "User not found")
        return user

    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_model)
    def put(self, user_id: str):
        """Update a user."""

        payload = api.payload or {}
        facade = _get_facade()
        try:
            user = facade.update_user(user_id, payload)
        except ValueError as exc:
            abort(400, str(exc))
        if user is None:
            abort(404, "User not found")
        return user


__all__ = ["api"]
