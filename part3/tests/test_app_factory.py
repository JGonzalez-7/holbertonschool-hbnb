"""Tests for the HBnB Part 3 application factory."""

from app import create_app
from config import DevelopmentConfig, TestingConfig


def test_create_app_uses_named_configuration():
    """Named configurations should resolve through the config registry."""
    app = create_app("testing")

    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == TestingConfig.SQLALCHEMY_DATABASE_URI


def test_create_app_accepts_configuration_class():
    """The factory should also accept a config class directly."""
    app = create_app(DevelopmentConfig)

    assert app.config["DEBUG"] is True
    assert app.config["JWT_SECRET_KEY"] == DevelopmentConfig.JWT_SECRET_KEY
