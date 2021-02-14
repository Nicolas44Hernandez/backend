"""Exercises management API."""

import logging
from datetime import datetime
from bson.objectid import ObjectId

from flask_smorest import Page
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask import Response
from marshmallow import Schema
from marshmallow.fields import Str, Int

from .blueprint import bp
from backend.model.data_model import Exercise

logger = logging.getLogger(__name__)


class CursorPage(Page):
    """ Page management."""

    @property
    def item_count(self):
        return self.collection.count()


class ExerciseArgsSchema(Schema):
    """ Query schema for Exercise API."""

    # Exercise name
    name = Str(required=True, description="backhand rolling", example="infield")
    # Exercise section
    section = Str(required=True, description="The training section", example="infield")
    # exercise dificulty (0-5)
    dificulty = Int(
        required=True, description="The training dificulty (0-5)", example=4
    )
    # training duration in minutes
    duration = Int(
        required=True, description="The training durationin minutes", example=30
    )
    # Training description
    description = Str(
        required=True,
        description="The training description",
        example="this is a training description",
    )
    # url video
    video = Str(
        required=True,
        description="The training video url",
        example="https://www.youtube.com/watch?v=J-nK0fZV7-8",
    )


class ExerciseSchema(ExerciseArgsSchema):
    """ Query schema for Exercise API query args."""

    # Exercise id
    _id = Str(required=True, data_key="id", attribute="id")


class ExerciseListArgsSchema(Schema):
    """ Query schema for exercises list API."""

    # exercise section
    section = Str(description="The training section", example="infield")


@bp.route("")
class ExercisesList(MethodView):
    """ API to list exercises """

    @bp.arguments(
        ExerciseListArgsSchema, location="query",
    )
    @bp.response(
        ExerciseSchema(many=True), description="The exercises list",
    )  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    @bp.paginate(CursorPage)
    # @jwt_required
    def get(self, args):
        """List all exercises
        Select all the exercises.
        If section specified, select the exercises from the section.
        """
        logger.debug("get exercise list ")
        query = {}

        if "section" in args:
            logger.debug("section=%s", args["section"])
            query["section"] = args["section"]

        exercises = Exercise.objects(**query)  # pylint: disable=no-member

        return exercises


@bp.route(
    "/<exercise_id>",
    parameters=[
        {
            "name": "exercise_id",
            "description": "The id of the exercise to retrieve",
            "example": "507f1f77bcf86cd799439011",
            "in": "path",
        }
    ],
)
class SingleExercise(MethodView):
    """ API to get/remove an exercise """

    @bp.response(ExerciseSchema)  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def get(self, exercise_id):
        """Get a single exercise """

        logger.debug("Get exercise with id=%s", exercise_id)

        exercises = Exercise.objects.get_or_404(
            id=ObjectId(exercise_id)
        )  # pylint: disable=no-member

        return exercises

    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def delete(self, exercise_id):
        """delete a single exercise """

        logger.debug("Delete exercise with id=%s", exercise_id)

        Exercise.objects.get_or_404(
            id=ObjectId(exercise_id)
        ).delete()  # pylint: disable=no-member

        return Response(status=200)


@bp.route("/create")
class Exercises(MethodView):
    """ API to create or update an exercise """

    @bp.arguments(
        ExerciseArgsSchema, description="The new exercise in json",
    )
    @bp.response(
        ExerciseSchema, description="The new exercise in json",
    )  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def put(self, put_data):
        """Create a new  exercise,return exercise in json"""

        logger.debug("Create a new exercise, data:")
        logger.debug(str(put_data))

        exercise = Exercise(
            name=put_data["name"],
            section=put_data["section"],
            dificulty=put_data["dificulty"],
            duration=put_data["duration"],
            description=put_data["description"],
            creation_date=datetime.now().date(),
            video=put_data["video"],
        ).save()

        return exercise
