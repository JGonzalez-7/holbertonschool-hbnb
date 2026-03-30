"""Shared pytest fixtures for Part 4."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.services.backend import BackendResponse


class FakeBackendClient:
    """Predictable backend client used by the test suite."""

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def request(self, method, path, *, token=None, json=None, params=None):
        self.calls.append(
            {
                "method": method,
                "path": path,
                "token": token,
                "json": json,
                "params": params,
            }
        )

        if method == "POST" and path == "/auth/login":
            if json == {"email": "user@example.com", "password": "secret123"}:
                return BackendResponse(200, {"access_token": "token-123"})
            return BackendResponse(401, {"message": "Invalid email or password"})

        if method == "GET" and path == "/auth/protected" and token == "token-123":
            return BackendResponse(
                200,
                {
                    "message": "Access granted",
                    "user_id": "user-1",
                    "is_admin": False,
                },
            )

        if method == "GET" and path == "/places/":
            return BackendResponse(
                200,
                [
                    {
                        "id": "place-1",
                        "name": "Coastal Loft",
                        "description": "Bright and airy",
                        "price": 120.0,
                        "latitude": 18.4,
                        "longitude": -66.1,
                        "owner_id": "owner-1",
                        "owner": {
                            "id": "owner-1",
                            "first_name": "Lena",
                            "last_name": "Stone",
                            "email": "lena@example.com",
                            "is_admin": False,
                        },
                        "reviews": [],
                        "amenities": [{"id": "a1", "name": "WiFi"}],
                        "average_rating": None,
                    }
                ],
            )

        if method == "GET" and path == "/places/place-1":
            return BackendResponse(
                200,
                {
                    "id": "place-1",
                    "name": "Coastal Loft",
                    "description": "Bright and airy",
                    "price": 120.0,
                    "latitude": 18.4,
                    "longitude": -66.1,
                    "owner_id": "owner-1",
                    "owner": {
                        "id": "owner-1",
                        "first_name": "Lena",
                        "last_name": "Stone",
                        "email": "lena@example.com",
                        "is_admin": False,
                    },
                    "reviews": [
                        {
                            "id": "review-1",
                            "rating": 5,
                            "comment": "Excellent stay",
                            "user_id": "user-2",
                            "place_id": "place-1",
                        }
                    ],
                    "amenities": [{"id": "a1", "name": "WiFi"}],
                    "average_rating": 5.0,
                },
            )

        if method == "GET" and path == "/amenities/":
            return BackendResponse(
                200,
                [{"id": "a1", "name": "WiFi"}, {"id": "a2", "name": "Pool"}],
            )

        if method == "GET" and path == "/users/user-2":
            return BackendResponse(
                200,
                {
                    "id": "user-2",
                    "first_name": "Casey",
                    "last_name": "Ray",
                    "email": "casey@example.com",
                    "is_admin": False,
                },
            )

        if method == "POST" and path == "/reviews/" and token == "token-123":
            return BackendResponse(
                201,
                {
                    "id": "review-2",
                    "rating": json["rating"],
                    "comment": json["comment"],
                    "user_id": "user-1",
                    "place_id": json["place_id"],
                },
            )

        return BackendResponse(404, {"message": "Not found"})


@pytest.fixture
def app():
    app = create_app("testing")
    app.extensions["backend_client"] = FakeBackendClient()
    return app


@pytest.fixture
def client(app):
    return app.test_client()
