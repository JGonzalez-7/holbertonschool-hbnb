"""Association tables for SQLAlchemy relationship mappings."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Table, Column, String

from app import db


place_amenity = Table(
    "place_amenity",
    db.metadata,
    Column("place_id", String(36), ForeignKey("places.id"), primary_key=True),
    Column("amenity_id", String(36), ForeignKey("amenities.id"), primary_key=True),
)


__all__ = ["place_amenity"]
