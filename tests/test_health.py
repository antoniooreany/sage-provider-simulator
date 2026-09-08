"""Tests for the GET /health endpoint.

Traces to: FR-207, AC-SIM-001
"""


def test_health_returns_200(client):
    """GET /health returns HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_status_ok(client):
    """GET /health body is {"status": "ok"}."""
    response = client.get("/health")
    data = response.get_json()
    assert data == {"status": "ok"}


def test_health_content_type_is_json(client):
    """GET /health returns application/json content type."""
    response = client.get("/health")
    assert response.content_type == "application/json"


def test_health_requires_no_auth(client):
    """GET /health does not require X-API-Key authentication."""
    # Deliberately omit any auth header — should still succeed.
    response = client.get("/health")
    assert response.status_code == 200
