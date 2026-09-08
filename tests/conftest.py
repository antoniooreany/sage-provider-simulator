"""Shared test fixtures for the Sage Provider Simulator."""

import pytest

from app import create_app


class TestConfig:
    """Configuration for tests — uses a known, non-secret test API key."""

    TESTING = True
    PROVIDER_API_KEY = "test-api-key-not-a-secret"


# Convenience constant for test API key — matches TestConfig.
TEST_API_KEY = "test-api-key-not-a-secret"


@pytest.fixture()
def app():
    """Create an application instance configured for testing."""
    app = create_app(config_object=TestConfig)
    yield app


@pytest.fixture()
def client(app):
    """Provide a Flask test client."""
    return app.test_client()
