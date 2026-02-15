"""Domain model base classes and exports."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict
from uuid import uuid4


class BaseModel:
    """Common fields and helpers for domain entities."""

    def __init__(
        self,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = str(id or uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def touch(self) -> None:
        """Refresh the `updated_at` timestamp."""

        self.updated_at = datetime.utcnow()

    def update(self, **kwargs: Any) -> None:
        """Assign provided attributes and bump `updated_at`."""

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.touch()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize base fields; subclasses can extend."""

        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity

__all__ = ["BaseModel", "User", "Place", "Review", "Amenity"]
