"""Exercises management API."""

import logging
from datetime import datetime
from bson.objectid import ObjectId

from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask import Response
from marshmallow import Schema
from marshmallow.fields import Str, Int, List, Nested, Date

from .blueprint import bp
from backend.model.data_model import Exercise, Stage, Training

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
    # Training  date
    date = Date(
        required=True,
        description="The etraining date ('YYYY-MM-DD HH:MM:SS')",
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


class TrainingPostSchema(TrainingSchema):
    # training id
    _id = Str(required=True, data_key="id", attribute="id")


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
        date=training["date"],
        place=training["place"],
        nb_stages=training["nb_stages"],
        tags=training["tags"],
        stages=training_stages,
    )


@bp.route("")
class NewTraining(MethodView):
    """ API to create / delete / update  a new training """

    # TODO: logs

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

    @bp.arguments(
        TrainingPostSchema, description="The training to modify in json",
    )
    @bp.response(
        TrainingSchema, description="The modified training in json",
    )  # pylint: disable=no-self-use
    @bp.doc(security=[{"bearerAuth": []}], responses={401: "UNAUTHORIZED"})
    # TODO: authentification
    # @jwt_required
    def post(self, post_data):
        """Modify a training, return training in json"""
        new_training = create_training(post_data)

        training = Training.objects.get_or_404(id=post_data["id"]).modify(
            category=new_training.category,
            date=new_training.date,
            place=new_training.place,
            nb_stages=len(new_training.stages),
            stages=new_training.stages,
            tags=new_training.tags,
        )  # pylint: disable=no-member"""

        return training
