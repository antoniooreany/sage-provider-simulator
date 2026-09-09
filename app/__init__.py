from flask import Flask


def create_app(config_object="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    from app.errors import register_error_handlers
    register_error_handlers(app)

    from app.blueprints.health import health_bp
    from app.blueprints.invoices import invoices_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(invoices_bp)

    return app
