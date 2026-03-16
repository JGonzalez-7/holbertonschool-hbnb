"""Place-specific SQLAlchemy repository."""

from __future__ import annotations

from app.models import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository[Place]):
    """Repository with place-specific lookup helpers."""

    def __init__(self) -> None:
        super().__init__(Place)

    def get_by_owner(self, owner_id: str) -> list[Place]:
        """Return places for a specific owner."""
        return self.filter_by_fields(owner_id=owner_id)


__all__ = ["PlaceRepository"]
