from bson import ObjectId
from datetime import datetime, timezone

from backend.training.model import (
    Training,
    Stage,
    Exercise,
)

DESCRIPTION = (
    "Hola soy una descripcion de un ejercicio \n "
    "Hola soy una descripcion de un ejercicio \n "
    "Hola soy una descripcion de un ejercicio \n "
    "Hola soy una descripcion de un ejercicio \n "
    "Hola soy una descripcion de un ejercicio \n "
)


def test_save_exercise(app, mongo):
    with app.app_context():
        assert mongo["exercise"].count() == 0
        Exercise(
            oid=ObjectId(),
            section="infield",
            dificulty=5,
            duration=30,
            description=DESCRIPTION,
            video="https://www.youtube.com/watch?v=CTavtQnB6Rk&t=335s",
        ).save()

        assert mongo["exercise"].count_documents({"section": "infield"}) == 1


def test_save_training(app, mongo):
    with app.app_context():
        assert mongo["exercise"].count() == 0
        assert mongo["training"].count() == 0

        exercise = Exercise(
            oid=ObjectId(),
            section="infield",
            dificulty=5,
            duration=30,
            description=DESCRIPTION,
            video="https://www.youtube.com/watch?v=CTavtQnB6Rk&t=335s",
        ).save()

        exercises_list = []
        exercises_list.append(str(exercise.oid))

        stage = Stage(oid=ObjectId(), nb_exercises=1, exercises=exercises_list)

        Training(
            date=datetime.now(timezone.utc),
            place="Hawks Stadium",
            nb_stages=1,
            stages=[stage],
            tags=["infield", "backhand"],
        ).save()

        assert mongo["training"].count_documents({"nb_stages": 1}) == 1

