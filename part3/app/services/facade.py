"""Facade coordinating repository-backed user operations."""

from __future__ import annotations

from typing import Any

from app.models import Amenity, Place, Review, User
from app.persistence import (
    AmenityRepository,
    PlaceRepository,
    ReviewRepository,
    UserRepository,
)


class HBnBFacade:
    """Service facade for repository-backed persistence workflows."""

    def __init__(self) -> None:
        self.users = UserRepository()
        self.places = PlaceRepository()
        self.reviews = ReviewRepository()
        self.amenities = AmenityRepository()

    def create_user(self, data: dict[str, Any]) -> User:
        """Create and persist a user after validation."""
        User.validate_payload(data)

        email = str(data["email"]).strip().lower()
        if self.users.get_by_email(email):
            raise ValueError("User already exists")

        user = User(
            first_name=str(data["first_name"]).strip(),
            last_name=str(data["last_name"]).strip(),
            email=email,
            password_hash="",
            is_admin=bool(data.get("is_admin", False)),
        )
        user.password = str(data["password"])
        return self.users.save(user)

    def list_users(self) -> list[User]:
        """Return all users ordered by email."""
        return sorted(self.users.list(), key=lambda user: user.email)

    def get_user(self, user_id: str) -> User | None:
        """Retrieve a single user."""
        return self.users.get(user_id)

    def update_user(self, user_id: str, data: dict[str, Any]) -> User | None:
        """Apply user updates and persist them."""
        user = self.users.get(user_id)
        if user is None:
            return None

        if "first_name" in data:
            first_name = data["first_name"]
            if not isinstance(first_name, str) or not first_name.strip():
                raise ValueError("first_name must be a non-empty string")
            user.first_name = first_name.strip()

        if "last_name" in data:
            last_name = data["last_name"]
            if not isinstance(last_name, str) or not last_name.strip():
                raise ValueError("last_name must be a non-empty string")
            user.last_name = last_name.strip()

        if "email" in data:
            email = str(data["email"]).strip().lower()
            if "@" not in email:
                raise ValueError("email must contain '@'")
            existing = self.users.get_by_email(email)
            if existing is not None and existing.id != user.id:
                raise ValueError("User already exists")
            user.email = email

        if "password" in data:
            user.password = str(data["password"])

        if "is_admin" in data:
            if not isinstance(data["is_admin"], bool):
                raise ValueError("is_admin must be a boolean")
            user.is_admin = data["is_admin"]

        return self.users.save(user)

    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        return self.users.delete(user_id)

    def create_place(self, data: dict[str, Any]) -> Place:
        """Create and persist a place."""
        Place.validate_payload(data)
        owner_id = str(data["owner_id"])
        owner = self.users.get(owner_id)
        if owner is None:
            raise ValueError("Owner not found")

        amenities: list[Amenity] = []
        for amenity_id in data.get("amenity_ids", []):
            amenity = self.amenities.get(str(amenity_id))
            if amenity is None:
                raise ValueError("Amenity not found")
            amenities.append(amenity)

        place = Place(
            name=str(data["name"]).strip(),
            description=data.get("description"),
            price=float(data["price"]),
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            owner_id=owner_id,
        )
        place.owner = owner
        place.amenities = amenities
        return self.places.save(place)

    def list_places(self) -> list[Place]:
        """Return all places."""
        return sorted(self.places.list(), key=lambda place: place.created_at)

    def get_place(self, place_id: str) -> Place | None:
        """Retrieve a place."""
        return self.places.get(place_id)

    def update_place(self, place_id: str, data: dict[str, Any]) -> Place | None:
        """Apply place updates and persist them."""
        place = self.places.get(place_id)
        if place is None:
            return None
        update_data = dict(data)
        if "amenity_ids" in data:
            amenities: list[Amenity] = []
            for amenity_id in data["amenity_ids"] or []:
                amenity = self.amenities.get(str(amenity_id))
                if amenity is None:
                    raise ValueError("Amenity not found")
                amenities.append(amenity)
            place.amenities = amenities
            update_data.pop("amenity_ids", None)
        place.update_from_payload(update_data)
        return self.places.save(place)

    def delete_place(self, place_id: str) -> bool:
        """Delete a place."""
        return self.places.delete(place_id)

    def create_review(self, data: dict[str, Any]) -> Review:
        """Create and persist a review."""
        Review.validate_payload(data)
        user_id = str(data["user_id"])
        place_id = str(data["place_id"])

        user = self.users.get(user_id)
        if user is None:
            raise ValueError("User not found")
        place = self.places.get(place_id)
        if place is None:
            raise ValueError("Place not found")

        review = Review(
            rating=int(data["rating"]),
            comment=str(data["comment"]).strip(),
            user_id=user_id,
            place_id=place_id,
        )
        review.author = user
        review.place = place
        return self.reviews.save(review)

    def list_reviews(self) -> list[Review]:
        """Return all reviews."""
        return sorted(self.reviews.list(), key=lambda review: review.created_at)

    def list_reviews_for_place(self, place_id: str) -> list[Review]:
        """Return reviews for a place."""
        return sorted(self.reviews.get_by_place(place_id), key=lambda review: review.created_at)

    def get_review(self, review_id: str) -> Review | None:
        """Retrieve a review."""
        return self.reviews.get(review_id)

    def get_review_by_user_and_place(self, user_id: str, place_id: str) -> Review | None:
        """Retrieve the review for a user/place pair."""
        return self.reviews.get_by_user_and_place(user_id, place_id)

    def update_review(self, review_id: str, data: dict[str, Any]) -> Review | None:
        """Apply review updates and persist them."""
        review = self.reviews.get(review_id)
        if review is None:
            return None
        review.update_from_payload(data)
        return self.reviews.save(review)

    def delete_review(self, review_id: str) -> bool:
        """Delete a review."""
        return self.reviews.delete(review_id)

    def create_amenity(self, data: dict[str, Any]) -> Amenity:
        """Create and persist an amenity."""
        name = Amenity.validate_name(data.get("name"))
        if self.amenities.get_by_name(name) is not None:
            raise ValueError("Amenity already exists")
        amenity = Amenity(name=name)
        return self.amenities.save(amenity)

    def list_amenities(self) -> list[Amenity]:
        """Return all amenities."""
        return sorted(self.amenities.list(), key=lambda amenity: amenity.name.lower())

    def get_amenity(self, amenity_id: str) -> Amenity | None:
        """Retrieve an amenity."""
        return self.amenities.get(amenity_id)

    def update_amenity(self, amenity_id: str, data: dict[str, Any]) -> Amenity | None:
        """Apply amenity updates and persist them."""
        amenity = self.amenities.get(amenity_id)
        if amenity is None:
            return None
        name = Amenity.validate_name(data.get("name"))
        existing = self.amenities.get_by_name(name)
        if existing is not None and existing.id != amenity.id:
            raise ValueError("Amenity already exists")
        amenity.name = name
        return self.amenities.save(amenity)

    def delete_amenity(self, amenity_id: str) -> bool:
        """Delete an amenity."""
        amenity = self.amenities.get(amenity_id)
        if amenity is None:
            return False
        amenity.places.clear()
        return self.amenities.delete(amenity_id)

    def serialize_place(self, place: Place) -> dict[str, Any]:
        """Serialize a place with ORM-managed relationship data."""
        return place.to_dict()


__all__ = ["HBnBFacade"]
