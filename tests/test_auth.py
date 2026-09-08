"""Tests for X-API-Key authentication on /api/v1/ endpoints.

Traces to: FR-202, FR-208, AC-SIM-003
"""

from tests.conftest import TEST_API_KEY


def test_invoices_returns_401_without_api_key(client):
    """GET /api/v1/invoices without X-API-Key returns 401."""
    response = client.get("/api/v1/invoices")
    assert response.status_code == 401


def test_invoices_returns_401_with_invalid_api_key(client):
    """GET /api/v1/invoices with an invalid X-API-Key returns 401."""
    response = client.get(
        "/api/v1/invoices",
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


def test_invoices_401_body_is_json_error(client):
    """401 response body contains structured JSON error."""
    response = client.get("/api/v1/invoices")
    data = response.get_json()
    assert data is not None
    assert "error" in data
    assert data["error"] == "Unauthorized"
    assert "message" in data


def test_invoices_returns_200_with_valid_api_key(client):
    """GET /api/v1/invoices with valid X-API-Key returns 200."""
    response = client.get(
        "/api/v1/invoices",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 200


def test_health_remains_unauthenticated(client):
    """GET /health does not require X-API-Key (regression guard)."""
    response = client.get("/health")
    assert response.status_code == 200
