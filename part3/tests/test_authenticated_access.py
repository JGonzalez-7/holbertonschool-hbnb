"""Tests for authenticated access rules in Part 3."""

from __future__ import annotations

from app import create_app, db
from app.models import Place, Review, User


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


def test_public_reads_and_authenticated_place_ownership_rules():
    app = create_app("testing")
    owner = _create_user(app, "owner@example.com", "secret123")
    stranger = _create_user(app, "stranger@example.com", "secret456")

    with app.test_client() as client:
        public_list = client.get("/api/v1/places/")
        unauthorized_create = client.post(
            "/api/v1/places/",
            json={
                "name": "Villa",
                "description": "Ocean view",
                "price": 120.0,
                "latitude": 18.0,
                "longitude": -66.0,
            },
        )

        owner_token = _login(client, owner.email, "secret123")
        create_response = client.post(
            "/api/v1/places/",
            json={
                "name": "Villa",
                "description": "Ocean view",
                "price": 120.0,
                "latitude": 18.0,
                "longitude": -66.0,
            },
            headers={"Authorization": f"Bearer {owner_token}"},
        )

        place_id = create_response.get_json()["id"]
        public_item = client.get(f"/api/v1/places/{place_id}")

        stranger_token = _login(client, stranger.email, "secret456")
        forbidden_update = client.put(
            f"/api/v1/places/{place_id}",
            json={"name": "Hijacked"},
            headers={"Authorization": f"Bearer {stranger_token}"},
        )
        owner_update = client.put(
            f"/api/v1/places/{place_id}",
            json={"name": "Updated Villa"},
            headers={"Authorization": f"Bearer {owner_token}"},
        )
        forbidden_delete = client.delete(
            f"/api/v1/places/{place_id}",
            headers={"Authorization": f"Bearer {stranger_token}"},
        )
        owner_delete = client.delete(
            f"/api/v1/places/{place_id}",
            headers={"Authorization": f"Bearer {owner_token}"},
        )

    assert public_list.status_code == 200
    assert unauthorized_create.status_code == 401
    assert create_response.status_code == 201
    assert create_response.get_json()["owner_id"] == owner.id
    assert public_item.status_code == 200
    assert forbidden_update.status_code == 403
    assert owner_update.status_code == 200
    assert owner_update.get_json()["name"] == "Updated Villa"
    assert forbidden_delete.status_code == 403
    assert owner_delete.status_code == 204


def test_review_rules_and_review_ownership_checks():
    app = create_app("testing")
    owner = _create_user(app, "owner@example.com", "secret123")
    reviewer = _create_user(app, "reviewer@example.com", "secret456")
    intruder = _create_user(app, "intruder@example.com", "secret789")

    with app.app_context():
        place = Place(
            name="Cabin",
            description="Quiet",
            price=75.0,
            latitude=18.2,
            longitude=-66.1,
            owner_id=owner.id,
        )
        db.session.add(place)
        db.session.commit()
        db.session.refresh(place)
        place_id = place.id

    with app.test_client() as client:
        public_reviews = client.get("/api/v1/reviews/")

        owner_token = _login(client, owner.email, "secret123")
        own_review = client.post(
            "/api/v1/reviews/",
            json={"rating": 5, "comment": "Mine", "place_id": place_id},
            headers={"Authorization": f"Bearer {owner_token}"},
        )

        reviewer_token = _login(client, reviewer.email, "secret456")
        create_review = client.post(
            "/api/v1/reviews/",
            json={"rating": 4, "comment": "Nice stay", "place_id": place_id},
            headers={"Authorization": f"Bearer {reviewer_token}"},
        )
        review_id = create_review.get_json()["id"]

        duplicate_review = client.post(
            "/api/v1/reviews/",
            json={"rating": 3, "comment": "Again", "place_id": place_id},
            headers={"Authorization": f"Bearer {reviewer_token}"},
        )

        intruder_token = _login(client, intruder.email, "secret789")
        forbidden_update = client.put(
            f"/api/v1/reviews/{review_id}",
            json={"comment": "Changed"},
            headers={"Authorization": f"Bearer {intruder_token}"},
        )
        owner_update = client.put(
            f"/api/v1/reviews/{review_id}",
            json={"comment": "Updated", "rating": 5},
            headers={"Authorization": f"Bearer {reviewer_token}"},
        )
        forbidden_delete = client.delete(
            f"/api/v1/reviews/{review_id}",
            headers={"Authorization": f"Bearer {intruder_token}"},
        )
        owner_delete = client.delete(
            f"/api/v1/reviews/{review_id}",
            headers={"Authorization": f"Bearer {reviewer_token}"},
        )

    assert public_reviews.status_code == 200
    assert own_review.status_code == 400
    assert create_review.status_code == 201
    assert duplicate_review.status_code == 400
    assert forbidden_update.status_code == 403
    assert owner_update.status_code == 200
    assert owner_update.get_json()["rating"] == 5
    assert forbidden_delete.status_code == 403
    assert owner_delete.status_code == 204


def test_user_can_only_update_their_own_profile_without_email_or_password():
    app = create_app("testing")
    alice = _create_user(app, "alice@example.com", "secret123")
    bob = _create_user(app, "bob@example.com", "secret456")

    with app.test_client() as client:
        alice_token = _login(client, alice.email, "secret123")
        bob_token = _login(client, bob.email, "secret456")

        own_update = client.put(
            f"/api/v1/users/{alice.id}",
            json={"first_name": "Alicia", "last_name": "Stone"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )
        forbidden_update = client.put(
            f"/api/v1/users/{alice.id}",
            json={"first_name": "Mallory"},
            headers={"Authorization": f"Bearer {bob_token}"},
        )
        invalid_fields = client.put(
            f"/api/v1/users/{alice.id}",
            json={"email": "new@example.com"},
            headers={"Authorization": f"Bearer {alice_token}"},
        )

    assert own_update.status_code == 200
    assert own_update.get_json()["first_name"] == "Alicia"
    assert own_update.get_json()["last_name"] == "Stone"
    assert forbidden_update.status_code == 403
    assert invalid_fields.status_code == 400

    with app.app_context():
        updated_user = db.session.get(User, alice.id)
        assert updated_user.email == "alice@example.com"
        assert updated_user.verify_password("secret123") is True


def test_place_and_review_queries_reflect_deleted_resources():
    app = create_app("testing")
    owner = _create_user(app, "owner@example.com", "secret123")
    reviewer = _create_user(app, "reviewer@example.com", "secret456")

    with app.app_context():
        place = Place(
            name="Loft",
            description="City center",
            price=90.0,
            latitude=18.3,
            longitude=-66.2,
            owner_id=owner.id,
        )
        review = Review(
            rating=4,
            comment="Great",
            user_id=reviewer.id,
            place_id=place.id,
        )
        db.session.add_all([place, review])
        db.session.commit()
        place_id = place.id
        review_id = review.id

    with app.test_client() as client:
        owner_token = _login(client, owner.email, "secret123")
        reviewer_token = _login(client, reviewer.email, "secret456")
        delete_review = client.delete(
            f"/api/v1/reviews/{review_id}",
            headers={"Authorization": f"Bearer {reviewer_token}"},
        )
        delete_place = client.delete(
            f"/api/v1/places/{place_id}",
            headers={"Authorization": f"Bearer {owner_token}"},
        )
        missing_review = client.get(f"/api/v1/reviews/{review_id}")
        missing_place = client.get(f"/api/v1/places/{place_id}")

    assert delete_review.status_code == 204
    assert delete_place.status_code == 204
    assert missing_review.status_code == 404
    assert missing_place.status_code == 404
