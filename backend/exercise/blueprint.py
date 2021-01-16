""" API entrypoints for events."""

from flask_smorest import Blueprint

bp = Blueprint(
    "exercise",
    __name__,
    url_prefix="/api/v1/exercises",
    description="This endpoint allows to put and retrieve exercises info.",
)
