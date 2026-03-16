"""Tests for the Part 3 user API."""

from __future__ import annotations

from app import create_app, db
from app.models import User


def test_post_users_hashes_password_and_hides_it():
    app = create_app("testing")

    with app.app_context():
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password_hash="",
            is_admin=True,
        )
        admin.password = "secret123"
        db.session.add(admin)
        db.session.commit()

    with app.test_client() as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "secret123"},
        )
        access_token = login_response.get_json()["access_token"]
        response = client.post(
            "/api/v1/users/",
            json={
                "first_name": "Alice",
                "last_name": "Doe",
                "email": "alice@example.com",
                "password": "secret123",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == "alice@example.com"
    assert "password" not in data
    assert "password_hash" not in data

    with app.app_context():
        user = User.query.filter_by(email="alice@example.com").first()
        assert user is not None
        assert user.password_hash != "secret123"
        assert user.verify_password("secret123") is True


def test_get_users_does_not_return_password_fields():
    app = create_app("testing")

    with app.app_context():
        user = User(
            first_name="Bob",
            last_name="Smith",
            email="bob@example.com",
            password_hash="",
        )
        user.password = "topsecret"
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    with app.test_client() as client:
        list_response = client.get("/api/v1/users/")
        item_response = client.get(f"/api/v1/users/{user_id}")

    assert list_response.status_code == 200
    assert item_response.status_code == 200

    list_payload = list_response.get_json()
    item_payload = item_response.get_json()

    assert list_payload[0]["email"] == "bob@example.com"
    assert "password" not in list_payload[0]
    assert "password_hash" not in list_payload[0]
    assert "password" not in item_payload
    assert "password_hash" not in item_payload
