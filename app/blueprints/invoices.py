import json
import os

from flask import Blueprint, jsonify, request

from app.auth import require_api_key

invoices_bp = Blueprint("invoices", __name__, url_prefix="/api/v1")

@invoices_bp.route("/invoices", methods=["GET"])
@require_api_key
def get_invoices():
    if request.args.get("simulate_error") == "500":
        return jsonify({"error": "Internal Server Error", "message": "Simulated provider failure."}), 500

    # Load fixtures from the project root's fixtures folder.
    # We find the project root by going up two levels from this file (app/blueprints)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    fixture_path = os.path.join(base_dir, "fixtures", "invoices.json")

    try:
        with open(fixture_path) as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
