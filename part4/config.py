"""Configuration classes for the HBnB Part 4 web client."""

from __future__ import annotations

import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/api/v1")
    BACKEND_TIMEOUT = float(os.getenv("BACKEND_TIMEOUT", "10"))
    TESTING = False
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    BACKEND_API_URL = "http://backend.test/api/v1"
    BACKEND_TIMEOUT = 1.0


class ProductionConfig(Config):
    pass


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

