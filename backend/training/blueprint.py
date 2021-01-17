""" API entrypoints for events."""

from flask_smorest import Blueprint

bp = Blueprint(
    "training",
    __name__,
    url_prefix="/api/v1/trainings",
    description="This endpoint allows to put and retrieve trainings info.",
)
