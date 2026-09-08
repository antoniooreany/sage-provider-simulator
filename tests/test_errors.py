"""Tests for simulated error scenarios.

Traces to: FR-205, FR-208, AC-SIM-004
"""

from tests.conftest import TEST_API_KEY


def test_simulate_error_500_returns_500(client):
    """GET /api/v1/invoices?simulate_error=500 with valid key returns 500."""
    response = client.get(
        "/api/v1/invoices?simulate_error=500",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 500


def test_simulate_error_500_body_is_json(client):
    """500 response body contains structured JSON with error and message."""
    response = client.get(
        "/api/v1/invoices?simulate_error=500",
        headers={"X-API-Key": TEST_API_KEY},
    )
    data = response.get_json()
    assert data is not None
    assert "error" in data
    assert "message" in data
    assert data["error"] == "Internal Server Error"
    assert data["message"] == "Simulated provider failure."


def test_simulate_error_500_requires_auth(client):
    """simulate_error=500 still requires valid X-API-Key (returns 401 without)."""
    response = client.get("/api/v1/invoices?simulate_error=500")
    assert response.status_code == 401


def test_normal_request_still_returns_200(client):
    """Requests without simulate_error still return 200 with invoices."""
    response = client.get(
        "/api/v1/invoices",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "invoices" in data
