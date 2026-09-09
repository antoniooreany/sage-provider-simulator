from functools import wraps

from flask import current_app, jsonify, request


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != current_app.config["PROVIDER_API_KEY"]:
            return jsonify({"error": "Unauthorized", "message": "Valid X-API-Key header required."}), 401
        return f(*args, **kwargs)
    return decorated_function
