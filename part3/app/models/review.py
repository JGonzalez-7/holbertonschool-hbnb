"""Review model for HBnB Part 3."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Review(BaseModel):
    """Review persisted in the relational database."""

    __tablename__ = "reviews"
    __table_args__ = (UniqueConstraint("user_id", "place_id", name="uq_review_user_place"),)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    place_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("places.id"),
        nullable=False,
        index=True,
    )
    author: Mapped["User"] = relationship("User", back_populates="reviews")
    place: Mapped["Place"] = relationship("Place", back_populates="reviews")

    @staticmethod
    def validate_payload(data: dict[str, object]) -> None:
        """Validate required review fields."""
        rating = data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")

        comment = data.get("comment")
        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("comment must be a non-empty string")

        user_id = data.get("user_id")
        if user_id is not None and (not isinstance(user_id, str) or not user_id.strip()):
            raise ValueError("user_id must be a non-empty string")

        place_id = data.get("place_id")
        if place_id is not None and (not isinstance(place_id, str) or not place_id.strip()):
            raise ValueError("place_id must be a non-empty string")

    def update_from_payload(self, data: dict[str, object]) -> None:
        """Apply a partial update after validating allowed fields."""
        allowed_fields = {"rating", "comment"}
        invalid_fields = sorted(set(data) - allowed_fields)
        if invalid_fields:
            raise ValueError(f"Unsupported field(s): {', '.join(invalid_fields)}")

        candidate = {
            "rating": data.get("rating", self.rating),
            "comment": data.get("comment", self.comment),
        }
        self.validate_payload(candidate)

        self.rating = int(candidate["rating"])
        self.comment = str(candidate["comment"]).strip()

    def to_dict(self) -> dict[str, object]:
        """Serialize the review."""
        data = super().to_dict()
        data.update(
            {
                "rating": self.rating,
                "comment": self.comment,
                "user_id": self.user_id,
                "place_id": self.place_id,
            }
        )
        return data


__all__ = ["Review"]
