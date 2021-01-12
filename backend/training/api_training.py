"""Sites management API."""

import logging

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from marshmallow import Schema
from marshmallow.fields import Str, List, Nested

from .blueprint import bp
from .model import Training, Stage, Exercise

logger = logging.getLogger(__name__)


@bp.route("")
class Sites(MethodView):
    """APi retrieving all known Sites."""

    @bp.response()
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    @jwt_required
    def get(self):  # pylint: disable=no-self-use
        """List all sites."""

        return

