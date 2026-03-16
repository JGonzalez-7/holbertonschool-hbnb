"""Amenity model for HBnB Part 3."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import place_amenity
from app.models.base import BaseModel


class Amenity(BaseModel):
    """Amenity persisted in the relational database."""

    __tablename__ = "amenities"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    places: Mapped[list["Place"]] = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities",
    )

    @staticmethod
    def validate_name(name: object) -> str:
        """Validate and normalize an amenity name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        return name.strip()

    def to_dict(self) -> dict[str, object]:
        """Serialize the amenity."""
        data = super().to_dict()
        data.update({"name": self.name})
        return data


__all__ = ["Amenity"]
