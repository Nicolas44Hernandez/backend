from bson.objectid import ObjectId
from datetime import datetime


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
