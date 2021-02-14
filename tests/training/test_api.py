from datetime import datetime

from tests.fill_date_base import create_exercise, create_training, create_stage


def test_get_training(client, mongo):

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

    # init training collection
    stage = create_stage(exercises=exercises, duration=60)
    training = create_training(
        stages=[stage], date_time=datetime.now(), _id="11111f77bcf86cd799430001"
    )
    mongo["training"].insert_one(training)

    # verify creation in mongo DB
    training_1 = mongo["training"].find_one()
    _id = str(training_1["_id"])

    response = client.get("/api/v1/trainings/" + _id)

    assert response.status_code == 200
    # verify update in mongo DB
    assert mongo["training"].count() == 1
    training = mongo["training"].find_one()
    assert training_1 == training


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
    date_time = datetime.now()

    # Create a new training
    response = client.put(
        "/api/v1/trainings",
        json={
            "category": "18U",
            "date_time": date_time.isoformat(),
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
    assert date_time.replace(microsecond=0) == training["date_time"].replace(
        microsecond=0
    )
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

    # init training collection
    stage = create_stage(exercises=exercises, duration=60)
    training = create_training(
        stages=[stage], date_time=datetime.now(), _id="11111f77bcf86cd799430001"
    )
    mongo["training"].insert_one(training)

    # verify creation in mongo DB
    assert mongo["training"].count() == 1
    training_1 = mongo["training"].find_one()
    assert "18U" in training_1["category"]
    assert "Hawks Stadium" in training["place"]
    assert 1 == training_1["nb_stages"]
    assert 1 == len(training_1["stages"])
    assert 6 == training_1["stages"][0]["nb_exercises"]
    assert 6 == len(training_1["stages"][0]["exercises"])

    date_time = datetime.now()

    response = client.post(
        "/api/v1/trainings/" + str(training_1["_id"]),
        json={
            "category": "15U",
            "date_time": date_time.isoformat(),
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


def test_delete_training(client, mongo):

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

    # init training collection
    stage = create_stage(exercises=exercises, duration=60)
    training = create_training(
        stages=[stage], date_time=datetime.now(), _id="11111f77bcf86cd799430001"
    )
    mongo["training"].insert_one(training)

    # verify creation in mongo DB
    assert mongo["training"].count() == 1
    training_1 = mongo["training"].find_one()
    assert "18U" in training_1["category"]
    assert "Hawks Stadium" in training["place"]
    assert 1 == training_1["nb_stages"]
    assert 1 == len(training_1["stages"])
    assert 6 == training_1["stages"][0]["nb_exercises"]
    assert 6 == len(training_1["stages"][0]["exercises"])

    response = client.delete("/api/v1/trainings/" + str(training_1["_id"]))
    assert response.status_code == 200
    # verify update in mongo DB
    assert mongo["training"].count() == 0

