from bson.objectid import ObjectId
from datetime import datetime

from backend.model.data_model import (
    Training,
    Stage,
    Exercise,
)


def test_put_training(client, mongo):

    # init the exercises collection
    mongo["exercise"].insert_many(
        [
            create_exercise("507f1f77bcf86cd799439011", section="infield"),
            create_exercise("507f1f77bcf86cd799439012", section="outfield"),
            create_exercise("507f1f77bcf86cd799439013", section="pitching"),
            create_exercise("507f1f77bcf86cd799439014", section="infield"),
            create_exercise("507f1f77bcf86cd799439015", section="outfield"),
            create_exercise("507f1f77bcf86cd799439016", section="infield"),
        ]
    )
    date = datetime.now().date()
    # Create a new training
    response = client.put(
        "/api/v1/trainings",
        json={
            "category": "18U",
            "date": date.isoformat(),
            "place": "Hawks Stadium",
            "nb_stages": 2,
            "tags": ["15U", "infield", "oufield", "arm", "rollings"],
            "stages": [
                {
                    "nb_exercises": 2,
                    "exercises": [
                        {"id": "507f1f77bcf86cd799439011"},
                        {"id": "507f1f77bcf86cd799439012"},
                    ],
                },
                {
                    "nb_exercises": 3,
                    "exercises": [
                        {"id": "507f1f77bcf86cd799439013"},
                        {"id": "507f1f77bcf86cd799439011"},
                        {"id": "507f1f77bcf86cd799439015"},
                    ],
                },
            ],
        },
    )

    assert response.status_code == 200
    # verify creation in mongo DB
    assert mongo["training"].count() == 1
    training = mongo["training"].find_one()
    assert "18U" in training["category"]
    assert date == training["date"].date()
    assert "Hawks Stadium" in training["place"]
    assert 2 == training["nb_stages"]
    assert 2 == len(training["stages"])
    assert 2 == training["stages"][0]["nb_exercises"]
    assert 2 == len(training["stages"][0]["exercises"])
    assert 3 == training["stages"][1]["nb_exercises"]
    assert 3 == len(training["stages"][1]["exercises"])


def test_post_modify_training(client, mongo):

    exercises = [
        create_exercise("507f1f77bcf86cd799439011", section="infield"),
        create_exercise("507f1f77bcf86cd799439012", section="outfield"),
        create_exercise("507f1f77bcf86cd799439013", section="pitching"),
        create_exercise("507f1f77bcf86cd799439014", section="infield"),
        create_exercise("507f1f77bcf86cd799439015", section="outfield"),
        create_exercise("507f1f77bcf86cd799439016", section="infield"),
    ]
    # init the exercises collection
    mongo["exercise"].insert_many(exercises)

    stage = create_stage(exercises=exercises, duration=60)
    training = insert_training(stages=[stage], date=datetime.now().date())

    # verify creation in mongo DB
    assert mongo["training"].count() == 1
    training_1 = mongo["training"].find_one()
    assert "18U" in training_1["category"]
    assert "Hawks Stadium" in training["place"]
    assert 1 == training_1["nb_stages"]
    assert 1 == len(training_1["stages"])
    assert 6 == training_1["stages"][0]["nb_exercises"]
    assert 6 == len(training_1["stages"][0]["exercises"])

    date = datetime.now().date()

    response = client.post(
        "/api/v1/trainings",
        json={
            "id": str(training.id),
            "category": "15U",
            "date": date.isoformat(),
            "place": "Chateau Giron",
            "nb_stages": 2,
            "tags": ["15U", "infield", "oufield", "arm", "rollings"],
            "stages": [
                {"nb_exercises": 1, "exercises": [{"id": "507f1f77bcf86cd799439012"}]},
                {"nb_exercises": 1, "exercises": [{"id": "507f1f77bcf86cd799439015"}]},
            ],
        },
    )
    assert response.status_code == 200
    # verify update in mongo DB
    assert mongo["training"].count() == 1
    training = mongo["training"].find_one()
    assert "15U" in training["category"]
    assert "Chateau Giron" in training["place"]
    assert 2 == training["nb_stages"]
    assert 2 == len(training["stages"])
    assert 1 == training["stages"][0]["nb_exercises"]
    assert 1 == len(training["stages"][0]["exercises"])
    assert 1 == training["stages"][1]["nb_exercises"]
    assert 1 == len(training["stages"][1]["exercises"])


def create_exercise(_id: str, name: str = "ex name", section: str = "infield"):
    return {
        "_id": ObjectId(_id),
        "name": "backhand rolling",
        "section": section,
        "dificulty": 3,
        "duration": 30,
        "description": "hit backhand rollings",
        "creation_date": datetime.now(),
        "video": "https://www.youtube.com/watch?v=J-nK0fZV7-8",
    }


def create_stage(exercises: [], duration: int = 60):
    exercises_list = []

    for exercise in exercises:
        exercise = Exercise(
            id=exercise["_id"],
            name=exercise["name"],
            section=exercise["section"],
            dificulty=exercise["dificulty"],
            duration=exercise["duration"],
            description=exercise["description"],
            creation_date=exercise["creation_date"],
            video=exercise["video"],
        ).save()
        exercises_list.append(str(exercise.id))

    return Stage(
        duration=duration, nb_exercises=len(exercises), exercises=exercises_list
    )


def insert_training(
    stages: [], date: datetime, category: str = "18U", place: str = "Hawks Stadium"
):
    training = Training(
        category=category,
        date=date,
        place=place,
        nb_stages=len(stages),
        stages=stages,
        tags=["tag1", "tag2", "tag3"],
    ).save()

    return training
