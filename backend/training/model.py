""" Event models for Mongo documents."""
from flask_mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    FloatField,
    IntField,
    ListField,
    ObjectIdField,
    StringField,
)


class Exercise(Document):
    """
    Define an exercise 
    """

    # the identifier
    oid = ObjectIdField(required=True)
    # Training section
    section = StringField(required=True)
    # exercise dificulty (0-5)
    dificulty = IntField(required=True)
    # training duration in minutes
    duration = IntField(required=True)
    # Training description
    description = StringField(required=True)
    # url video
    video = StringField()


class Stage(EmbeddedDocument):
    """
    Define an Stage
    """

    # the identifier
    oid = ObjectIdField(required=True)
    # number of exercises
    nb_exercises = IntField(required=True)
    # exercises list
    exercises = ListField(StringField(), required=True)


class Training(Document):
    """
    Define a Training
    """

    # Training  date
    date = DateTimeField(required=True)
    # Training place
    place = StringField(required=True)
    # number of stages
    nb_stages = IntField(required=True)
    # the list of stages
    stages = ListField(EmbeddedDocumentField(Stage))
    # tags
    tags = ListField(StringField())

