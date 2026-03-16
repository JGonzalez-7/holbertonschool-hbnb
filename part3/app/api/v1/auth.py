"""Authentication endpoints for HBnB Part 3."""

from __future__ import annotations

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from app.models import User

api = Namespace("auth", description="Authentication operations")

login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

token_model = api.model(
    "TokenResponse",
    {
        "access_token": fields.String(required=True),
    },
)

protected_model = api.model(
    "ProtectedResponse",
    {
        "message": fields.String(required=True),
        "user_id": fields.String(required=True),
        "is_admin": fields.Boolean(required=True),
    },
)


@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.marshal_with(token_model)
    def post(self):
        """Authenticate a user and return a JWT access token."""
        payload = api.payload or {}
        email = str(payload.get("email", "")).strip().lower()
        password = str(payload.get("password", ""))

        if not email or not password:
            api.abort(400, "email and password are required")

        user = User.query.filter_by(email=email).first()
        if user is None or not user.verify_password(password):
            api.abort(401, "Invalid email or password")

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"is_admin": user.is_admin},
        )
        return {"access_token": access_token}, 200


@api.route("/protected")
class Protected(Resource):
    @jwt_required()
    @api.marshal_with(protected_model)
    def get(self):
        """Verify the caller's JWT token and return embedded claims."""
        claims = get_jwt()
        return {
            "message": "Access granted",
            "user_id": get_jwt_identity(),
            "is_admin": claims.get("is_admin", False),
        }


__all__ = ["api"]
