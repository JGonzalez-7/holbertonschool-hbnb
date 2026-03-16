"""SQLAlchemy-backed repository implementation."""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

from app import db
from app.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class SQLAlchemyRepository(Generic[T]):
    """Generic repository backed by the Flask-SQLAlchemy session."""

    def __init__(self, model: type[T]) -> None:
        self.model = model
        self.session = db.session

    def save(self, entity: T) -> T:
        """Persist an entity."""
        self.session.add(entity)
        self.session.commit()
        return entity

    def get(self, entity_id) -> T | None:
        """Retrieve an entity by primary key."""
        return self.session.get(self.model, entity_id)

    def delete(self, entity_id) -> bool:
        """Delete an entity by primary key."""
        entity = self.get(entity_id)
        if entity is None:
            return False
        self.session.delete(entity)
        self.session.commit()
        return True

    def list(self) -> list[T]:
        """Return all entities for the configured model."""
        return self.session.query(self.model).all()

    def clear(self) -> None:
        """Delete all entities for the configured model."""
        self.session.query(self.model).delete()
        self.session.commit()

    def find_first(self, predicate: Callable[[T], bool]) -> T | None:
        """Return the first entity matching a Python predicate."""
        return next((item for item in self.list() if predicate(item)), None)

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        """Return entities matching a Python predicate."""
        return [item for item in self.list() if predicate(item)]

    def find_by_fields(self, **kwargs) -> T | None:
        """Return the first entity matching the provided field values."""
        return self.session.query(self.model).filter_by(**kwargs).first()

    def filter_by_fields(self, **kwargs) -> list[T]:
        """Return all entities matching the provided field values."""
        return list(self.session.query(self.model).filter_by(**kwargs).all())


__all__ = ["SQLAlchemyRepository"]
