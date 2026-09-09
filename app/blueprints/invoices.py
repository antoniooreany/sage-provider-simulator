import json
import math
import os

from flask import Blueprint, jsonify, make_response, request

from app.auth import require_api_key

invoices_bp = Blueprint("invoices", __name__, url_prefix="/api/v1")


@invoices_bp.route("/invoices", methods=["GET"])
@require_api_key
def get_invoices():
    # 1. Error simulation handling (takes precedence over pagination validation)
    simulate_error = request.args.get("simulate_error")
    if simulate_error == "500":
        return jsonify({"error": "Internal Server Error", "message": "Simulated provider failure."}), 500

    if simulate_error == "429":
        response = make_response(
            jsonify(
                {
                    "error": "Too Many Requests",
                    "message": "Simulated rate limit exceeded. Please retry after 5 seconds.",
                }
            ),
            429,
        )
        response.headers["Retry-After"] = "5"
        return response

    # 2. Duplicate pagination parameter checks
    page_args = request.args.getlist("page")
    if len(page_args) > 1:
        return jsonify({"error": "Bad Request", "message": "Duplicate 'page' query parameter."}), 400

    per_page_args = request.args.getlist("per_page")
    if len(per_page_args) > 1:
        return jsonify({"error": "Bad Request", "message": "Duplicate 'per_page' query parameter."}), 400

    # 3. Validate pagination parameters
    page = 1
    if page_args:
        try:
            val = int(page_args[0])
            if val < 1 or str(val) != page_args[0].strip():
                raise ValueError
            page = val
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": "Invalid 'page' parameter: must be an integer >= 1.",
                    }
                ),
                400,
            )

    per_page = 10
    if per_page_args:
        try:
            val = int(per_page_args[0])
            if val < 1 or val > 100 or str(val) != per_page_args[0].strip():
                raise ValueError
            per_page = val
        except ValueError:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": "Invalid 'per_page' parameter: must be an integer between 1 and 100.",
                    }
                ),
                400,
            )

    # 4. Load fixtures
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    fixture_path = os.path.join(base_dir, "fixtures", "invoices.json")

    try:
        with open(fixture_path) as f:
            data = json.load(f)
        all_invoices = data.get("invoices", [])
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    total_items = len(all_invoices)
    total_pages = math.ceil(total_items / per_page) if total_items > 0 else 0

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_invoices = all_invoices[start_idx:end_idx]

    return (
        jsonify(
            {
                "invoices": paginated_invoices,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_items": total_items,
                    "total_pages": total_pages,
                },
            }
        ),
        200,
    )
