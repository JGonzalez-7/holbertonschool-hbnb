"""Tests for JWT authentication in Part 3."""

from __future__ import annotations

from app import create_app, db
from app.models import User


def test_login_returns_access_token_for_valid_credentials():
    app = create_app("testing")

    with app.app_context():
        user = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password_hash="",
            is_admin=True,
        )
        user.password = "secret123"
        db.session.add(user)
        db.session.commit()

    with app.test_client() as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "secret123"},
        )

    assert response.status_code == 200
    payload = response.get_json()
    assert "access_token" in payload
    assert isinstance(payload["access_token"], str)
    assert payload["access_token"]


def test_login_rejects_invalid_credentials():
    app = create_app("testing")

    with app.app_context():
        user = User(
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            password_hash="",
        )
        user.password = "correct-password"
        db.session.add(user)
        db.session.commit()

    with app.test_client() as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "alice@example.com", "password": "wrong-password"},
        )

    assert response.status_code == 401


def test_protected_endpoint_requires_valid_jwt_and_exposes_claims():
    app = create_app("testing")

    with app.app_context():
        user = User(
            first_name="Bob",
            last_name="Smith",
            email="bob@example.com",
            password_hash="",
            is_admin=True,
        )
        user.password = "topsecret"
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with app.test_client() as client:
        unauthorized = client.get("/api/v1/auth/protected")
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "bob@example.com", "password": "topsecret"},
        )
        access_token = login_response.get_json()["access_token"]
        authorized = client.get(
            "/api/v1/auth/protected",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    assert unauthorized.status_code == 401
    assert authorized.status_code == 200
    payload = authorized.get_json()
    assert payload["message"] == "Access granted"
    assert payload["user_id"] == user_id
    assert payload["is_admin"] is True
