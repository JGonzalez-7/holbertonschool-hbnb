"""Basic configuration stub."""

import os


class Config:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


__all__ = ["Config", "TestingConfig"]
