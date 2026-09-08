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
