"""Tests for the GET /api/v1/invoices endpoint.

Traces to: FR-201, AC-SIM-002
"""

from tests.conftest import TEST_API_KEY

REQUIRED_INVOICE_FIELDS = {
    "id",
    "date",
    "due_date",
    "status",
    "currency",
    "total_amount",
    "contact_name",
}


def _get_invoices(client):
    """Helper to GET /api/v1/invoices with valid auth."""
    return client.get(
        "/api/v1/invoices",
        headers={"X-API-Key": TEST_API_KEY},
    )


def test_invoices_response_contains_invoices_key(client):
    """Response JSON has an 'invoices' key."""
    response = _get_invoices(client)
    data = response.get_json()
    assert "invoices" in data


def test_invoices_returns_at_least_three(client):
    """At least 3 fixture invoices are returned."""
    response = _get_invoices(client)
    data = response.get_json()
    assert len(data["invoices"]) >= 3


def test_invoices_have_required_fields(client):
    """Each invoice contains all required fields."""
    response = _get_invoices(client)
    data = response.get_json()
    for invoice in data["invoices"]:
        assert REQUIRED_INVOICE_FIELDS.issubset(invoice.keys()), (
            f"Invoice {invoice.get('id', '?')} missing fields: "
            f"{REQUIRED_INVOICE_FIELDS - invoice.keys()}"
        )


def test_invoices_content_type_is_json(client):
    """Response content-type is application/json."""
    response = _get_invoices(client)
    assert response.content_type == "application/json"


def test_invoices_response_is_deterministic(client):
    """Two identical requests return the same data."""
    response_a = _get_invoices(client)
    response_b = _get_invoices(client)
    assert response_a.get_json() == response_b.get_json()


def test_invoices_have_distinct_ids(client):
    """Fixture invoices have distinct IDs."""
    response = _get_invoices(client)
    data = response.get_json()
    ids = [inv["id"] for inv in data["invoices"]]
    assert len(ids) == len(set(ids)), "Invoice IDs are not unique"


def test_invoices_default_pagination(client):
    """Default request includes pagination metadata (page=1, per_page=10)."""
    response = _get_invoices(client)
    assert response.status_code == 200
    data = response.get_json()
    assert "pagination" in data
    pagination = data["pagination"]
    assert pagination["page"] == 1
    assert pagination["per_page"] == 10
    assert pagination["total_items"] == 3
    assert pagination["total_pages"] == 1
    assert len(data["invoices"]) == 3


def test_invoices_pagination_slicing(client):
    """Explicit page and per_page slices fixture invoices correctly."""
    # Page 1 with per_page=2: should return 2 invoices (INV-001, INV-002)
    response_p1 = client.get(
        "/api/v1/invoices?page=1&per_page=2",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response_p1.status_code == 200
    data_p1 = response_p1.get_json()
    assert len(data_p1["invoices"]) == 2
    assert data_p1["invoices"][0]["id"] == "INV-001"
    assert data_p1["invoices"][1]["id"] == "INV-002"
    assert data_p1["pagination"] == {
        "page": 1,
        "per_page": 2,
        "total_items": 3,
        "total_pages": 2,
    }

    # Page 2 with per_page=2: should return 1 invoice (INV-003)
    response_p2 = client.get(
        "/api/v1/invoices?page=2&per_page=2",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response_p2.status_code == 200
    data_p2 = response_p2.get_json()
    assert len(data_p2["invoices"]) == 1
    assert data_p2["invoices"][0]["id"] == "INV-003"
    assert data_p2["pagination"] == {
        "page": 2,
        "per_page": 2,
        "total_items": 3,
        "total_pages": 2,
    }


def test_invoices_pagination_empty_page_beyond_final(client):
    """Requesting a page beyond the final page returns 200 with empty list."""
    response = client.get(
        "/api/v1/invoices?page=5&per_page=2",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["invoices"] == []
    assert data["pagination"] == {
        "page": 5,
        "per_page": 2,
        "total_items": 3,
        "total_pages": 2,
    }


def test_invoices_pagination_invalid_page_returns_400(client):
    """Invalid page parameter (< 1 or non-integer) returns 400 Bad Request."""
    for bad_page in ["0", "-1", "abc", "1.5"]:
        response = client.get(
            f"/api/v1/invoices?page={bad_page}",
            headers={"X-API-Key": TEST_API_KEY},
        )
        assert response.status_code == 400, f"Expected 400 for page={bad_page}"
        data = response.get_json()
        assert data.get("error") == "Bad Request"
        assert "message" in data


def test_invoices_pagination_invalid_per_page_returns_400(client):
    """Invalid per_page parameter (< 1, > 100, or non-integer) returns 400."""
    for bad_per_page in ["0", "-5", "101", "xyz", "2.0"]:
        response = client.get(
            f"/api/v1/invoices?per_page={bad_per_page}",
            headers={"X-API-Key": TEST_API_KEY},
        )
        assert response.status_code == 400, f"Expected 400 for per_page={bad_per_page}"
        data = response.get_json()
        assert data.get("error") == "Bad Request"
        assert "message" in data


def test_invoices_pagination_duplicate_page_returns_400(client):
    """Duplicate page query parameters return 400 Bad Request."""
    response = client.get(
        "/api/v1/invoices?page=1&page=2",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("error") == "Bad Request"
    assert "message" in data


def test_invoices_pagination_duplicate_per_page_returns_400(client):
    """Duplicate per_page query parameters return 400 Bad Request."""
    response = client.get(
        "/api/v1/invoices?per_page=5&per_page=10",
        headers={"X-API-Key": TEST_API_KEY},
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data.get("error") == "Bad Request"
    assert "message" in data


def test_invoices_pagination_requires_auth_before_validation(client):
    """Unauthenticated requests with invalid pagination return 401, not 400."""
    response = client.get("/api/v1/invoices?page=-1&per_page=invalid")
    assert response.status_code == 401
