from __future__ import annotations

from typing import List

from . import BaseModel
from .place import Place
from .review import Review


class User(BaseModel):
    """User domain entity."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        is_admin: bool = False,
        places: List[Place] | None = None,
        reviews: List[Review] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._validate(first_name, last_name, email, password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places: List[Place] = places or []
        self.reviews: List[Review] = reviews or []

    def update_profile(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> None:
        if first_name is not None:
            self._validate(first_name, self.last_name, self.email, self.password)
            self.first_name = first_name
        if last_name is not None:
            self._validate(self.first_name, last_name, self.email, self.password)
            self.last_name = last_name
        if email is not None:
            self._validate(self.first_name, self.last_name, email, self.password)
            self.email = email
        if password is not None:
            self._validate(self.first_name, self.last_name, self.email, password)
            self.password = password
        self.touch()

    def add_place(self, place: Place) -> None:
        if place not in self.places:
            self.places.append(place)
            self.touch()

    def add_review(self, review: Review) -> None:
        self.reviews.append(review)
        self.touch()

    @staticmethod
    def _validate(first_name: str, last_name: str, email: str, password: str) -> None:
        for field_name, value in [
            ("first_name", first_name),
            ("last_name", last_name),
            ("email", email),
            ("password", password),
        ]:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if "@" not in email:
            raise ValueError("email must contain '@'")

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "is_admin": self.is_admin,
                # Do not expose password in serialization
            }
        )
        return data


__all__ = ["User"]
