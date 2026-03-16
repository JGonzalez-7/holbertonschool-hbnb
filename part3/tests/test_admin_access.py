"""Tests for administrator access rules in Part 3."""

from __future__ import annotations

from app import create_app, db
from app.models import Amenity, Place, Review, User


def _create_user(app, email: str, password: str, is_admin: bool = False) -> User:
    with app.app_context():
        user = User(
            first_name=email.split("@", 1)[0].title(),
            last_name="User",
            email=email,
            password_hash="",
            is_admin=is_admin,
        )
        user.password = password
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


def _login(client, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.get_json()["access_token"]


def test_only_admin_can_create_users():
    app = create_app("testing")
    admin = _create_user(app, "admin@example.com", "secret123", is_admin=True)
    regular = _create_user(app, "user@example.com", "secret456")

    with app.test_client() as client:
        no_token = client.post(
            "/api/v1/users/",
            json={
                "first_name": "Alice",
                "last_name": "Doe",
                "email": "alice@example.com",
                "password": "pw123456",
            },
        )
        regular_token = _login(client, regular.email, "secret456")
        regular_attempt = client.post(
            "/api/v1/users/",
            json={
                "first_name": "Alice",
                "last_name": "Doe",
                "email": "alice@example.com",
                "password": "pw123456",
            },
            headers={"Authorization": f"Bearer {regular_token}"},
        )
        admin_token = _login(client, admin.email, "secret123")
        admin_attempt = client.post(
            "/api/v1/users/",
            json={
                "first_name": "Alice",
                "last_name": "Doe",
                "email": "alice@example.com",
                "password": "pw123456",
                "is_admin": True,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    assert no_token.status_code == 401
    assert regular_attempt.status_code == 403
    assert admin_attempt.status_code == 201
    assert admin_attempt.get_json()["is_admin"] is True


def test_admin_can_modify_any_user_including_email_and_password():
    app = create_app("testing")
    admin = _create_user(app, "admin@example.com", "secret123", is_admin=True)
    target = _create_user(app, "target@example.com", "secret456")

    with app.test_client() as client:
        admin_token = _login(client, admin.email, "secret123")
        response = client.put(
            f"/api/v1/users/{target.id}",
            json={
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated@example.com",
                "password": "newpassword",
                "is_admin": True,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["email"] == "updated@example.com"
    assert payload["is_admin"] is True

    with app.app_context():
        updated = db.session.get(User, target.id)
        assert updated.verify_password("newpassword") is True


def test_only_admin_can_manage_amenities():
    app = create_app("testing")
    admin = _create_user(app, "admin@example.com", "secret123", is_admin=True)
    regular = _create_user(app, "user@example.com", "secret456")

    with app.test_client() as client:
        public_list = client.get("/api/v1/amenities/")

        regular_token = _login(client, regular.email, "secret456")
        regular_attempt = client.post(
            "/api/v1/amenities/",
            json={"name": "WiFi"},
            headers={"Authorization": f"Bearer {regular_token}"},
        )

        admin_token = _login(client, admin.email, "secret123")
        admin_create = client.post(
            "/api/v1/amenities/",
            json={"name": "WiFi"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        amenity_id = admin_create.get_json()["id"]
        admin_update = client.put(
            f"/api/v1/amenities/{amenity_id}",
            json={"name": "Pool"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    assert public_list.status_code == 200
    assert regular_attempt.status_code == 403
    assert admin_create.status_code == 201
    assert admin_update.status_code == 200
    assert admin_update.get_json()["name"] == "Pool"


def test_admin_bypasses_place_and_review_ownership_restrictions():
    app = create_app("testing")
    admin = _create_user(app, "admin@example.com", "secret123", is_admin=True)
    owner = _create_user(app, "owner@example.com", "secret456")
    reviewer = _create_user(app, "reviewer@example.com", "secret789")

    with app.app_context():
        place = Place(
            name="Villa",
            description="Ocean view",
            price=150.0,
            latitude=18.4,
            longitude=-66.3,
            owner_id=owner.id,
        )
        review = Review(
            rating=4,
            comment="Nice place",
            user_id=reviewer.id,
            place_id=place.id,
        )
        db.session.add_all([place, review])
        db.session.commit()
        db.session.refresh(place)
        db.session.refresh(review)
        place_id = place.id
        review_id = review.id

    with app.test_client() as client:
        admin_token = _login(client, admin.email, "secret123")
        update_place = client.put(
            f"/api/v1/places/{place_id}",
            json={"name": "Admin Updated Villa"},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        update_review = client.put(
            f"/api/v1/reviews/{review_id}",
            json={"comment": "Admin updated", "rating": 5},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        delete_review = client.delete(
            f"/api/v1/reviews/{review_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        delete_place = client.delete(
            f"/api/v1/places/{place_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    assert update_place.status_code == 200
    assert update_place.get_json()["name"] == "Admin Updated Villa"
    assert update_review.status_code == 200
    assert update_review.get_json()["rating"] == 5
    assert delete_review.status_code == 204
    assert delete_place.status_code == 204


def test_admin_can_create_places_and_reviews_for_other_users():
    app = create_app("testing")
    admin = _create_user(app, "admin@example.com", "secret123", is_admin=True)
    owner = _create_user(app, "owner@example.com", "secret456")
    reviewer = _create_user(app, "reviewer@example.com", "secret789")

    with app.test_client() as client:
        admin_token = _login(client, admin.email, "secret123")
        place_response = client.post(
            "/api/v1/places/",
            json={
                "name": "Admin Created",
                "description": "Managed",
                "price": 99.0,
                "latitude": 18.5,
                "longitude": -66.4,
                "owner_id": owner.id,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        place_id = place_response.get_json()["id"]

        review_response = client.post(
            "/api/v1/reviews/",
            json={
                "rating": 5,
                "comment": "Admin created",
                "place_id": place_id,
                "user_id": reviewer.id,
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    assert place_response.status_code == 201
    assert place_response.get_json()["owner_id"] == owner.id
    assert review_response.status_code == 201
    assert review_response.get_json()["user_id"] == reviewer.id

    with app.app_context():
        assert db.session.query(Amenity).count() == 0
