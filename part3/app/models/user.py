"""User model for HBnB Part 3."""

from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import bcrypt
from app.models.base import BaseModel


class User(BaseModel):
    """Application user persisted in the relational database."""

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    places: Mapped[list["Place"]] = relationship(
        "Place",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="author",
        cascade="all, delete-orphan",
    )

    @property
    def password(self) -> str:
        """Prevent raw password reads from the model."""
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, raw_password: str) -> None:
        self._validate_password(raw_password)
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def verify_password(self, raw_password: str) -> bool:
        """Return whether a raw password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    def to_dict(self) -> dict[str, str]:
        """Serialize the user without exposing password data."""
        data = super().to_dict()
        data.update(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "is_admin": self.is_admin,
            }
        )
        return data

    @staticmethod
    def validate_payload(data: dict[str, object], require_password: bool = True) -> None:
        """Validate the incoming user payload."""
        required_fields = ["first_name", "last_name", "email"]
        if require_password:
            required_fields.append("password")

        for field_name in required_fields:
            value = data.get(field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        email = str(data.get("email", "")).strip()
        if "@" not in email:
            raise ValueError("email must contain '@'")

        if "is_admin" in data and not isinstance(data["is_admin"], bool):
            raise ValueError("is_admin must be a boolean")

        if require_password:
            User._validate_password(str(data["password"]))

    @staticmethod
    def _validate_password(raw_password: str) -> None:
        if not isinstance(raw_password, str) or not raw_password.strip():
            raise ValueError("password must be a non-empty string")


__all__ = ["User"]
