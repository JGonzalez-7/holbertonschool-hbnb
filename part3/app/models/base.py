"""Shared SQLAlchemy base model for HBnB Part 3 entities."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class BaseModel(db.Model):
    """Abstract base model with common identifier and timestamps."""

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        now = datetime.utcnow()
        if getattr(self, "id", None) is None:
            self.id = str(uuid.uuid4())
        if getattr(self, "created_at", None) is None:
            self.created_at = now
        if getattr(self, "updated_at", None) is None:
            self.updated_at = self.created_at

    def touch(self) -> None:
        """Refresh the update timestamp."""
        self.updated_at = datetime.utcnow()

    def update(self, **kwargs) -> None:
        """Assign attributes and refresh the update timestamp."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.touch()

    def to_dict(self) -> dict[str, object]:
        """Serialize common base fields."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


__all__ = ["BaseModel"]
