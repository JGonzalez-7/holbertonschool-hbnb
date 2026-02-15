from __future__ import annotations

from . import BaseModel


class Amenity(BaseModel):
    """Amenity domain entity."""

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self._validate_name(name)
        self.name = name

    def rename(self, name: str) -> None:
        self._validate_name(name)
        self.name = name
        self.touch()

    @staticmethod
    def _validate_name(name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")

    def to_dict(self):
        data = super().to_dict()
        data.update({"name": self.name})
        return data


__all__ = ["Amenity"]
