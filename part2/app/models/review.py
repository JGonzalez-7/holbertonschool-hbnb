from __future__ import annotations

from . import BaseModel


class Review(BaseModel):
    """Review domain entity."""

    def __init__(
        self, rating: int, comment: str, user_id: str, place_id: str, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._validate(rating, comment, user_id, place_id)
        self.rating = rating
        self.comment = comment
        self.user_id = user_id
        self.place_id = place_id

    def edit(self, rating: int | None = None, comment: str | None = None) -> None:
        if rating is not None:
            self._validate(rating, comment or self.comment, self.user_id, self.place_id)
            self.rating = rating
        if comment is not None:
            self.comment = comment
        self.touch()

    @staticmethod
    def _validate(rating: int, comment: str, user_id: str, place_id: str) -> None:
        if rating is None or not (1 <= rating <= 5):
            raise ValueError("rating must be between 1 and 5")
        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("comment must be a non-empty string")
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a non-empty string")
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("place_id must be a non-empty string")

    def to_dict(self):
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
