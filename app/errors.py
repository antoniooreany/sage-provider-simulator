from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({"error": "Not Found", "message": "The requested resource could not be found."}), 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        # We only want to handle generic errors that aren't already handled.
        # This will catch everything else.
        return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500
