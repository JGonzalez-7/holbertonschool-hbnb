"""User-specific SQLAlchemy repository."""

from __future__ import annotations

from app.models import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    """Repository with user-specific lookup helpers."""

    def __init__(self) -> None:
        super().__init__(User)

    def get_by_email(self, email: str) -> User | None:
        """Return the user matching the provided email."""
        normalized_email = email.strip().lower()
        return self.find_by_fields(email=normalized_email)


__all__ = ["UserRepository"]
