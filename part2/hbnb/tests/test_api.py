import sys
from pathlib import Path

import pytest

# Ensure the project root (containing the `app` package) is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def _create_user(client, email="alice@example.com"):
    resp = client.post(
        "/api/v1/users",
        json={
            "first_name": "Alice",
            "last_name": "Doe",
            "email": email,
            "password": "secret",
        },
    )
    assert resp.status_code == 201
    return resp.get_json()


def _create_amenity(client, name="Wifi"):
    resp = client.post("/api/v1/amenities", json={"name": name})
    assert resp.status_code == 201
    return resp.get_json()


def _create_place(client, owner_id, amenity_ids=None):
    amenity_ids = amenity_ids or []
    resp = client.post(
        "/api/v1/places",
        json={
            "name": "Beach House",
            "description": "Nice view",
            "price": 100.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": owner_id,
            "amenity_ids": amenity_ids,
        },
    )
    return resp


def _create_review(client, user_id, place_id, rating=5, comment="Great"):
    resp = client.post(
        "/api/v1/reviews",
        json={
            "rating": rating,
            "comment": comment,
            "user_id": user_id,
            "place_id": place_id,
        },
    )
    return resp


def test_user_crud_without_delete(client):
    user = _create_user(client)
    # list
    resp = client.get("/api/v1/users")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert "password" not in data[0]
    # get
    resp = client.get(f"/api/v1/users/{user['id']}")
    assert resp.status_code == 200
    # update
    resp = client.put(f"/api/v1/users/{user['id']}", json={"last_name": "Smith"})
    assert resp.status_code == 200
    assert resp.get_json()["last_name"] == "Smith"
    # delete not allowed -> 405
    resp = client.delete(f"/api/v1/users/{user['id']}")
    assert resp.status_code == 405


def test_amenity_create_update_list_no_delete(client):
    amenity = _create_amenity(client)
    resp = client.get("/api/v1/amenities")
    assert resp.status_code == 200
    assert resp.get_json()[0]["name"] == amenity["name"]
    # update
    resp = client.put(f"/api/v1/amenities/{amenity['id']}", json={"name": "Pool"})
    assert resp.status_code == 200
    assert resp.get_json()["name"] == "Pool"
    # delete not allowed
    resp = client.delete(f"/api/v1/amenities/{amenity['id']}")
    assert resp.status_code == 405


def test_place_create_requires_owner_and_returns_reviews_field(client):
    user = _create_user(client)
    amenity = _create_amenity(client)
    # create place
    resp = _create_place(client, owner_id=user["id"], amenity_ids=[amenity["id"]])
    assert resp.status_code == 201
    place = resp.get_json()
    assert place["owner"]["email"] == user["email"]
    assert place["amenities"][0]["id"] == amenity["id"]
    assert place["reviews"] == []
    # invalid owner -> 404
    resp_bad = _create_place(client, owner_id="missing-owner")
    assert resp_bad.status_code == 404


def test_review_crud_with_delete(client):
    user = _create_user(client, email="bob@example.com")
    amenity = _create_amenity(client, name="AC")
    place_resp = _create_place(client, owner_id=user["id"], amenity_ids=[amenity["id"]])
    place = place_resp.get_json()

    # create review
    resp = _create_review(client, user_id=user["id"], place_id=place["id"], rating=4, comment="Good")
    assert resp.status_code == 201
    review = resp.get_json()
    assert review["rating"] == 4

    # list
    resp = client.get("/api/v1/reviews")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1

    # update
    resp = client.put(f"/api/v1/reviews/{review['id']}", json={"comment": "Great", "rating": 5})
    assert resp.status_code == 200
    assert resp.get_json()["rating"] == 5

    # delete
    resp = client.delete(f"/api/v1/reviews/{review['id']}")
    assert resp.status_code == 204
    # ensure removed from place reviews
    place_get = client.get(f"/api/v1/places/{place['id']}")
    assert place_get.status_code == 200
    assert place_get.get_json()["reviews"] == []


def test_review_validation(client):
    user = _create_user(client, email="charlie@example.com")
    amenity = _create_amenity(client, name="TV")
    place_resp = _create_place(client, owner_id=user["id"], amenity_ids=[amenity["id"]])
    place = place_resp.get_json()

    # missing comment
    resp = _create_review(client, user_id=user["id"], place_id=place["id"], rating=3, comment="")
    assert resp.status_code == 400

    # bad rating
    resp = _create_review(client, user_id=user["id"], place_id=place["id"], rating=0, comment="bad")
    assert resp.status_code == 400
