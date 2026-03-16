"""Review-specific SQLAlchemy repository."""

from __future__ import annotations

from app.models import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository[Review]):
    """Repository with review-specific lookup helpers."""

    def __init__(self) -> None:
        super().__init__(Review)

    def get_by_place(self, place_id: str) -> list[Review]:
        """Return reviews for a specific place."""
        return self.filter_by_fields(place_id=place_id)

    def get_by_user_and_place(self, user_id: str, place_id: str) -> Review | None:
        """Return the review for a user/place pair if it exists."""
        return self.find_by_fields(user_id=user_id, place_id=place_id)


__all__ = ["ReviewRepository"]
