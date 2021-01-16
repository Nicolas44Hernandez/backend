""" App initialization module."""
import os
from flask import Flask
from backend import config, exercise
from backend.extension import api, socketio, mongo, jwt
from backend.config import Struct


def create_app(configs: Struct = None):
    """
    Create and configure the Flask app
    """
    app = Flask("backend")

    # load configuration
    if not configs:
        configs = os.getenv("CONFIG")
        configs = config.load_config_as_object(additional_config_files=configs)

    app.config.from_object(configs)

    register_extensions(app)
    register_blueprints(app)

    app.logger.info("App ready!!")  # pylint: disable=no-member

    return app


def register_extensions(app):
    """ Initialize App extensions."""
    jwt.init_app(app)
    app.logger.debug("jwt.init_app successfully processed.")

    mongo.init_app(app)
    app.logger.debug("mongo.init_app successfully processed.")

    socketio.init_app(app)
    app.logger.debug("socketio.init_app successfully processed.")


def register_blueprints(app):
    """ Store App APIs blueprints."""
    api.init_app(
        app,
        spec_kwargs={
            "info": {"description": "The `Backend` OpenAPI 3.0 specification."},
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                    }
                }
            },
        },
    )

    # register bluprints
    api.register_blueprint(exercise.blueprint.bp)


if __name__ == "__main__":
    socketio.run(create_app(), debug=True, use_reloader=False)
