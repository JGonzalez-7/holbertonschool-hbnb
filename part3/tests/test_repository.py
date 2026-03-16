"""Tests for the SQLAlchemy repository and facade."""

from __future__ import annotations

from datetime import datetime

from app import create_app
from app.persistence import (
    AmenityRepository,
    PlaceRepository,
    ReviewRepository,
    SQLAlchemyRepository,
    UserRepository,
)
from app.models import Amenity, BaseModel, Place, Review, User
from app.services import HBnBFacade


def test_base_model_provides_identifier_and_timestamps():
    app = create_app("testing")

    with app.app_context():
        user = User(
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            password_hash="",
        )
        user.password = "secret123"
        payload = user.to_dict()

        assert isinstance(user, BaseModel)
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert isinstance(payload["created_at"], str)
        assert isinstance(payload["updated_at"], str)


def test_sqlalchemy_repository_supports_basic_user_queries():
    app = create_app("testing")

    with app.app_context():
        repository = SQLAlchemyRepository(User)
        user = User(
            first_name="Alice",
            last_name="Doe",
            email="alice@example.com",
            password_hash="",
        )
        user.password = "secret123"
        repository.save(user)

        fetched = repository.get(user.id)
        by_email = repository.find_by_fields(email="alice@example.com")
        filtered = repository.filter_by_fields(is_admin=False)

        assert fetched is not None
        assert fetched.email == "alice@example.com"
        assert by_email is not None
        assert by_email.id == user.id
        assert len(filtered) == 1


def test_user_repository_supports_email_lookup():
    app = create_app("testing")

    with app.app_context():
        repository = UserRepository()
        user = User(
            first_name="Charlie",
            last_name="Brown",
            email="charlie@example.com",
            password_hash="",
        )
        user.password = "secret123"
        repository.save(user)

        fetched = repository.get_by_email("CHARLIE@example.com")

        assert fetched is not None
        assert fetched.id == user.id


def test_facade_uses_repository_for_user_create_and_update():
    app = create_app("testing")

    with app.app_context():
        facade = HBnBFacade()
        created = facade.create_user(
            {
                "first_name": "Bob",
                "last_name": "Smith",
                "email": "bob@example.com",
                "password": "secret123",
                "is_admin": False,
            }
        )
        updated = facade.update_user(
            created.id,
            {
                "first_name": "Bobby",
                "email": "bobby@example.com",
                "password": "newsecret",
            },
        )
        fetched = facade.get_user(created.id)

        assert created.email == "bob@example.com"
        assert created.verify_password("secret123") is True
        assert updated is not None
        assert updated.email == "bobby@example.com"
        assert updated.verify_password("newsecret") is True
        assert fetched is not None
        assert fetched.first_name == "Bobby"


def test_place_review_and_amenity_repositories_support_basic_crud():
    app = create_app("testing")

    with app.app_context():
        user_repo = UserRepository()
        place_repo = PlaceRepository()
        review_repo = ReviewRepository()
        amenity_repo = AmenityRepository()

        user = User(
            first_name="Dana",
            last_name="Owner",
            email="dana@example.com",
            password_hash="",
        )
        user.password = "secret123"
        user_repo.save(user)

        place = Place(
            name="Cabin",
            description="Quiet retreat",
            price=88.0,
            latitude=18.1,
            longitude=-66.1,
            owner_id=user.id,
        )
        place_repo.save(place)

        review = Review(
            rating=5,
            comment="Excellent",
            user_id=user.id,
            place_id=place.id,
        )
        review_repo.save(review)

        amenity = Amenity(name="WiFi")
        amenity_repo.save(amenity)

        assert place_repo.get_by_owner(user.id)[0].id == place.id
        assert review_repo.get_by_place(place.id)[0].id == review.id
        assert review_repo.get_by_user_and_place(user.id, place.id) is not None
        assert amenity_repo.get_by_name("WiFi") is not None


def test_facade_handles_place_review_and_amenity_crud():
    app = create_app("testing")

    with app.app_context():
        facade = HBnBFacade()
        user = facade.create_user(
            {
                "first_name": "Erin",
                "last_name": "User",
                "email": "erin@example.com",
                "password": "secret123",
            }
        )
        place = facade.create_place(
            {
                "name": "Studio",
                "description": "Compact",
                "price": 70.0,
                "latitude": 18.2,
                "longitude": -66.2,
                "owner_id": user.id,
            }
        )
        review = facade.create_review(
            {
                "rating": 4,
                "comment": "Nice",
                "user_id": user.id,
                "place_id": place.id,
            }
        )
        amenity = facade.create_amenity({"name": "Pool"})

        serialized_place = facade.serialize_place(place)

        assert facade.get_place(place.id) is not None
        assert facade.get_review(review.id) is not None
        assert facade.get_amenity(amenity.id) is not None
        assert serialized_place["owner"]["email"] == user.email
        assert serialized_place["reviews"][0]["id"] == review.id


def test_sqlalchemy_relationships_link_users_places_reviews_and_amenities():
    app = create_app("testing")

    with app.app_context():
        facade = HBnBFacade()
        owner = facade.create_user(
            {
                "first_name": "Olivia",
                "last_name": "Owner",
                "email": "olivia@example.com",
                "password": "secret123",
            }
        )
        reviewer = facade.create_user(
            {
                "first_name": "Riley",
                "last_name": "Reviewer",
                "email": "riley@example.com",
                "password": "secret123",
            }
        )
        wifi = facade.create_amenity({"name": "WiFi"})
        pool = facade.create_amenity({"name": "Pool"})
        place = facade.create_place(
            {
                "name": "Beach House",
                "description": "Ocean front",
                "price": 150.0,
                "latitude": 18.4,
                "longitude": -66.3,
                "owner_id": owner.id,
                "amenity_ids": [wifi.id, pool.id],
            }
        )
        review = facade.create_review(
            {
                "rating": 5,
                "comment": "Great stay",
                "user_id": reviewer.id,
                "place_id": place.id,
            }
        )

        refreshed_place = facade.get_place(place.id)
        refreshed_owner = facade.get_user(owner.id)
        refreshed_reviewer = facade.get_user(reviewer.id)

        assert refreshed_place is not None
        assert refreshed_owner is not None
        assert refreshed_reviewer is not None
        assert refreshed_place.owner is not None
        assert refreshed_place.owner.id == owner.id
        assert len(refreshed_place.reviews) == 1
        assert refreshed_place.reviews[0].id == review.id
        assert len(refreshed_place.amenities) == 2
        assert {amenity.name for amenity in refreshed_place.amenities} == {"WiFi", "Pool"}
        assert len(refreshed_owner.places) == 1
        assert refreshed_owner.places[0].id == place.id
        assert len(refreshed_reviewer.reviews) == 1
        assert refreshed_reviewer.reviews[0].id == review.id
