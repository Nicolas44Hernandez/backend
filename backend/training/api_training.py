"""Exercises management API."""
import logging
from functools import reduce
from datetime import datetime, timezone
from bson.objectid import ObjectId

from flask.views import MethodView

# from flask_jwt_extended import jwt_required
from marshmallow import Schema
from marshmallow.fields import Str, Int, List, Nested, Date, DateTime, Bool
from mongoengine.queryset.visitor import Q

from .blueprint import bp
from backend.model.data_model import Exercise, Stage, Training
from backend.apihelpers import DatetimeRangeQuerySchema


logger = logging.getLogger(__name__)


class ResumedExerciseSchema(Schema):
    # Exercise id
    _id = Str(required=True, data_key="id", attribute="id")
    # Exercise name
    name = Str(description="backhand rolling", example="infield")
    # Exercise section
    section = Str(description="The training section", example="infield")
    # exercise dificulty (0-5)
    dificulty = Int(description="The training dificulty (0-5)", example=4)
    # training duration in minutes
    duration = Int(description="The training durationin minutes", example=30)


class StageSchema(Schema):
    """ Schema for Stage """

    # number of exercises in the stage
    nb_exercises = Int(
        required=True, description="Number of exercises in the stage", example=4
    )
    # exercises in stage list
    exercises = List(Nested(ResumedExerciseSchema))


class TrainingSchema(Schema):
    """ Schema for Training """

    # Training category
    category = Str(required=True, description="The training category", example="15U")
    # Training  datetime
    date_time = DateTime(
        required=True,
        description="The training datetime ('YYYY-MM-DD HH:MM:SS')",
        example="2020-04-01T08:06:47.890Z",
    )
    # Training place
    place = Str(
        required=True, description="The training place", example="Hawks Stadium"
    )
    # number of stages
    nb_stages = Int(
        required=True, description="Number of stages in the training", example=1
    )
    # the list of stages
    stages = List(Nested(StageSchema))
    # tags
    tags = List(Str())


class TrainingIdSchema(Schema):
    # training id
    _id = Str(required=True, data_key="id", attribute="id")


class TrainingListArgsSchema(Schema):
    # Training category
    category = Str(required=True, description="The training category", example="15U")
    # date
    date = Date(description="date to query ('YYYY-MM-DD')", example="2020-04-01",)
    # week
    week = Bool(description="if true retrieves nex five days trainings", example=True)


def create_training(training: dict):
    training_stages = []
    for stage in training["stages"]:
        stage_exercises = []
        nb_exercises = 0
        longest_duration = 0
        for exercise in stage["exercises"]:
            # verify that the exercise exists
            ex = Exercise.objects.get_or_404(
                id=ObjectId(exercise["id"])
            )  # pylint: disable=no-member
            stage_exercises.append(exercise["id"])
            nb_exercises += 1
            if longest_duration < ex.duration:
                longest_duration = ex.duration

        training_stage = Stage(
            duration=longest_duration,
            nb_exercises=nb_exercises,
            exercises=stage_exercises,
        )
        training_stages.append(training_stage)

    return Training(
        category=training["category"],
        date_time=training["date_time"],
        place=training["place"],
        nb_stages=training["nb_stages"],
        tags=training["tags"],
        stages=training_stages,
    )


@bp.route(
    "/<training_id>",
    parameters=[
        {
            "name": "training_id",
            "description": "The id of the training to retrieve",
            "example": "507f1f77bcf86cd799439011",
            "in": "path",
        }
    ],
)
class ApiTraining(MethodView):
    """ API to create / delete / update  a new training """

    # TODO: logs

    @bp.arguments(
        TrainingSchema, description="The training to modify in json id required",
    )
    @bp.response(
        TrainingSchema, description="The modified training in json",
    )  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def post(self, post_data, training_id):
        """Modify a training, return training in json"""
        new_training = create_training(post_data)

        training = Training.objects.get_or_404(id=training_id).modify(
            category=new_training.category,
            date_time=new_training.date_time,
            place=new_training.place,
            nb_stages=len(new_training.stages),
            stages=new_training.stages,
            tags=new_training.tags,
        )  # pylint: disable=no-member"""

        return training

    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def delete(self, training_id):
        """Delete a training"""

        Training.objects.get_or_404(
            id=training_id
        ).delete()  # pylint: disable=no-member"""

        return {}

    @bp.response(TrainingSchema())
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def get(self, training_id):
        """Get a training """

        training = Training.objects.get_or_404(
            id=ObjectId(training_id)
        )  # pylint: disable=no-member"""

        return training


class GetTrainingListQuerySchema(DatetimeRangeQuerySchema):
    # Training category
    category = Str(description="The training category", example="18U", default="18U")


class ResumedTrainingSchema(Schema):
    """ Schema for Training """

    # Training category
    category = Str(required=True, description="The training category", example="15U")
    # Training  date
    date_time = DateTime(
        required=True,
        description="The etraining datetime ('YYYY-MM-DD HH:MM:SS')",
        example="2020-04-01T08:06:47.890Z",
    )
    # Training place
    place = Str(
        required=True, description="The training place", example="Hawks Stadium"
    )


@bp.route("")
class ApiNewTraining(MethodView):
    @bp.arguments(
        TrainingSchema, description="The new training in json",
    )
    @bp.response(
        TrainingSchema, description="The new training in json",
    )  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def put(self, put_data):
        """Create a new  training, return training in json"""

        training = create_training(put_data)
        training.save()
        return training

    @bp.arguments(GetTrainingListQuerySchema(), location="query")
    # TODO: logs
    @bp.response(
        ResumedTrainingSchema(many=True), description="The next trainings list in json",
    )  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def get(self, args):
        """get training list"""

        queries = []

        if "start" in args:
            queries.append(Q(date_time__gte=args["start"]))

        if "end" in args:
            queries.append(Q(date_time__lt=args["end"]))

        if "category" not in args:
            args["category"] = "18U"

        queries.append(Q(category=args["category"]))

        query = None

        if len(queries) == 1:
            query = queries[0]
        elif len(queries) >= 2:
            query = reduce(lambda q1, q2: q1 & q2, queries)

        return Training.objects(query)  # pylint: disable=no-member


class NexTrainingSchema(Schema):
    # Training category
    category = Str(
        description="The training category", required=True, example="18U", default="18U"
    )


@bp.route("/next")
class ApiNextTraining(MethodView):
    # TODO: logs
    @bp.arguments(NexTrainingSchema(), location="query")
    @bp.response(
        ResumedTrainingSchema(), description="The next training in json",
    )  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def get(self, args):
        """get next training"""
        now = datetime.now(timezone.utc)
        query = Q(date_time__gte=now)

        trainings = Training.objects(query)  # pylint: disable=no-member

        next_training_date = None
        next_training = None
        for training in trainings:
            if training["date_time"].astimezone(timezone.utc) > now:
                if training["category"] == args["category"]:
                    if next_training is None:
                        next_training = training
                        next_training_date = training["date_time"]
                    elif training["date_time"] < next_training_date:
                        next_training = training
                        next_training_date = training["date_time"]

        return next_training
