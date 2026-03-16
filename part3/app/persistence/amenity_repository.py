"""Amenity-specific SQLAlchemy repository."""

from __future__ import annotations

from app.models import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository[Amenity]):
    """Repository with amenity-specific lookup helpers."""

    def __init__(self) -> None:
        super().__init__(Amenity)

    def get_by_name(self, name: str) -> Amenity | None:
        """Return the amenity matching the provided name."""
        return self.find_by_fields(name=name.strip())

    def get_by_ids(self, amenity_ids: list[str]) -> list[Amenity]:
        """Return amenities for a set of ids."""
        if not amenity_ids:
            return []
        return list(self.session.query(self.model).filter(self.model.id.in_(amenity_ids)).all())


__all__ = ["AmenityRepository"]
