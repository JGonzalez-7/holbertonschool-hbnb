"""Place model for HBnB Part 3."""

from __future__ import annotations

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import place_amenity
from app.models.base import BaseModel


class Place(BaseModel):
    """Place persisted in the relational database."""

    __tablename__ = "places"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    owner_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    owner: Mapped["User"] = relationship("User", back_populates="places")
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan",
    )
    amenities: Mapped[list["Amenity"]] = relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
    )

    @staticmethod
    def validate_payload(data: dict[str, object]) -> None:
        """Validate required place fields."""
        name = data.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")

        price = data.get("price")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")

        latitude = data.get("latitude")
        if not isinstance(latitude, (int, float)) or not (-90 <= float(latitude) <= 90):
            raise ValueError("latitude must be between -90 and 90")

        longitude = data.get("longitude")
        if not isinstance(longitude, (int, float)) or not (-180 <= float(longitude) <= 180):
            raise ValueError("longitude must be between -180 and 180")

        description = data.get("description")
        if description is not None and not isinstance(description, str):
            raise ValueError("description must be a string")

        owner_id = data.get("owner_id")
        if owner_id is not None and (not isinstance(owner_id, str) or not owner_id.strip()):
            raise ValueError("owner_id must be a non-empty string")

    def update_from_payload(self, data: dict[str, object]) -> None:
        """Apply a partial update after validating allowed fields."""
        allowed_fields = {"name", "description", "price", "latitude", "longitude"}
        invalid_fields = sorted(set(data) - allowed_fields)
        if invalid_fields:
            raise ValueError(f"Unsupported field(s): {', '.join(invalid_fields)}")

        candidate = {
            "name": data.get("name", self.name),
            "description": data.get("description", self.description),
            "price": data.get("price", self.price),
            "latitude": data.get("latitude", self.latitude),
            "longitude": data.get("longitude", self.longitude),
        }
        self.validate_payload(candidate)

        self.name = str(candidate["name"]).strip()
        self.description = candidate["description"]
        self.price = float(candidate["price"])
        self.latitude = float(candidate["latitude"])
        self.longitude = float(candidate["longitude"])

    def average_rating(self) -> float | None:
        """Return the average review rating for the place."""
        if not self.reviews:
            return None
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    def to_dict(self) -> dict[str, object]:
        """Serialize the mapped place attributes."""
        data = super().to_dict()
        data.update(
            {
                "name": self.name,
                "description": self.description,
                "price": self.price,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "owner_id": self.owner_id,
                "owner": self.owner.to_dict() if self.owner else None,
                "reviews": [review.to_dict() for review in self.reviews],
                "amenities": [amenity.to_dict() for amenity in self.amenities],
                "average_rating": self.average_rating(),
            }
        )
        return data


__all__ = ["Place"]
