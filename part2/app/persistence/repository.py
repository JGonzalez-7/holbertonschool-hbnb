from __future__ import annotations

from typing import Callable, Dict, Generic, Iterable, List, Optional, TypeVar

from app.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class InMemoryRepository(Generic[T]):
    """Simple in-memory repository for entities with string IDs."""

    def __init__(self) -> None:
        self._items: Dict[str, T] = {}

    # CRUD
    def save(self, entity: T) -> T:
        self._items[entity.id] = entity
        return entity

    def get(self, entity_id: str) -> Optional[T]:
        return self._items.get(entity_id)

    def delete(self, entity_id: str) -> bool:
        return self._items.pop(entity_id, None) is not None

    def list(self) -> List[T]:
        return list(self._items.values())

    def clear(self) -> None:
        self._items.clear()

    # Queries
    def find_first(self, predicate: Callable[[T], bool]) -> Optional[T]:
        return next((item for item in self._items.values() if predicate(item)), None)

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._items.values() if predicate(item)]

    def find_by_fields(self, **kwargs) -> Optional[T]:
        """Find first entity whose attributes match all provided kwargs."""

        def matches(item: T) -> bool:
            return all(getattr(item, key, None) == value for key, value in kwargs.items())

        return self.find_first(matches)

    def filter_by_fields(self, **kwargs) -> List[T]:
        def matches(item: T) -> bool:
            return all(getattr(item, key, None) == value for key, value in kwargs.items())

        return self.filter(matches)


__all__ = ["InMemoryRepository"]
