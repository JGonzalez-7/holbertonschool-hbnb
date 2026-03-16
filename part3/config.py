"""Configuration classes for the HBnB Part 3 application."""

from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"


def _resolve_database_uri(env_var: str, default_filename: str) -> str:
    """Build a stable database URI for SQLite and pass through other engines."""
    database_url = os.getenv(env_var)
    if not database_url:
        if default_filename == ":memory:":
            return "sqlite:///:memory:"
        return f"sqlite:///{INSTANCE_DIR / default_filename}"

    if database_url.startswith("sqlite:///") and not database_url.startswith("sqlite:////"):
        relative_path = database_url.removeprefix("sqlite:///")
        return f"sqlite:///{(BASE_DIR / relative_path).resolve()}"

    return database_url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri("DATABASE_URL", "development.db")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri("TEST_DATABASE_URL", ":memory:")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri("DATABASE_URL", "production.db")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


__all__ = [
    "Config",
    "DevelopmentConfig",
    "ProductionConfig",
    "TestingConfig",
    "config",
]
