"""API proxy tests for Part 4."""

from __future__ import annotations


def test_login_stores_session_state(client):
    response = client.post(
        "/api/session/login",
        json={"email": "user@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "access_token": "token-123",
        "logged_in": True,
        "user_id": "user-1",
        "is_admin": False,
    }

    session_response = client.get("/api/session")
    assert session_response.status_code == 200
    assert session_response.get_json()["logged_in"] is False


def test_session_uses_token_cookie(client):
    client.set_cookie("token", "token-123")

    response = client.get("/api/session")

    assert response.status_code == 200
    assert response.get_json() == {
        "logged_in": True,
        "user_id": "user-1",
        "is_admin": False,
    }


def test_public_places_are_proxied(client):
    response = client.get("/api/places")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload[0]["name"] == "Coastal Loft"
    assert any(place["id"] == "demo-place-1" for place in payload)


def test_public_user_detail_is_proxied(client):
    response = client.get("/api/users/user-2")

    assert response.status_code == 200
    assert response.get_json()["first_name"] == "Casey"


def test_demo_place_and_demo_user_are_available(client):
    place_response = client.get("/api/places/demo-place-1")
    user_response = client.get("/api/users/demo-user-1")

    assert place_response.status_code == 200
    assert place_response.get_json()["name"] == "Canopy Loft Retreat"
    assert user_response.status_code == 200
    assert user_response.get_json()["first_name"] == "Nina"


def test_review_submission_requires_authentication(client):
    response = client.post(
        "/api/reviews",
        json={"place_id": "place-1", "rating": 5, "comment": "Excellent"},
    )

    assert response.status_code == 401
    assert response.get_json()["message"] == "Authentication required"


def test_review_submission_forwards_token_after_login(app, client):
    client.set_cookie("token", "token-123")

    response = client.post(
        "/api/reviews",
        json={"place_id": "place-1", "rating": 4, "comment": "Nice stay"},
    )

    assert response.status_code == 201
    assert response.get_json()["user_id"] == "user-1"
    assert app.extensions["backend_client"].calls[-1]["token"] == "token-123"
