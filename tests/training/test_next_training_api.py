from datetime import datetime, timedelta, timezone

from tests.fill_date_base import create_exercise, create_training, create_stage


# training dates
date_1 = datetime.now(timezone.utc) - timedelta(days=2)
date_2 = datetime.now(timezone.utc) - timedelta(days=1)
date_3 = datetime.now(timezone.utc) + timedelta(days=1)
date_4 = datetime.now(timezone.utc) + timedelta(days=2)


def test_get_next_training(client, mongo):
    fill_cololections(mongo)
    response = client.get("/api/v1/trainings/next?category=18U")
    assert response.status_code == 200
    training = response.get_json()
    assert date_3.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        training["date_time"]
    ).replace(microsecond=0, tzinfo=None)


def fill_cololections(mongo):

    # init the exercises collection
    exercises_1 = [
        create_exercise("507f1f77bcf86cd799439011", section="infield"),
        create_exercise("507f1f77bcf86cd799439012", section="outfield"),
    ]
    exercises_2 = [
        create_exercise("507f1f77bcf86cd799439013", section="infield"),
        create_exercise("507f1f77bcf86cd799439014", section="outfield"),
    ]
    exercises_3 = [
        create_exercise("507f1f77bcf86cd799439015", section="infield"),
        create_exercise("507f1f77bcf86cd799439016", section="outfield"),
    ]
    exercises_4 = [
        create_exercise("507f1f77bcf86cd799439017", section="infield"),
        create_exercise("507f1f77bcf86cd799439018", section="outfield"),
    ]
    exercises = exercises_1 + exercises_2 + exercises_3 + exercises_4

    mongo["exercise"].insert_many(exercises)

    # init training collection
    stage_1 = create_stage(exercises=exercises_1, duration=60)
    training_1 = create_training(
        stages=[stage_1], date_time=date_1, _id="11111f77bcf86cd799430001"
    )

    stage_2 = create_stage(exercises=exercises_2, duration=60)
    training_2 = create_training(
        stages=[stage_2], date_time=date_2, _id="11111f77bcf86cd799430002"
    )

    stage_3 = create_stage(exercises=exercises_3, duration=60)
    training_3 = create_training(
        stages=[stage_3], date_time=date_3, _id="11111f77bcf86cd799430002"
    )

    stage_4 = create_stage(exercises=exercises_4, duration=60)
    training_4 = create_training(
        stages=[stage_4], date_time=date_4, _id="11111f77bcf86cd799430002"
    )

    trainings = [training_1, training_2, training_3, training_4]

    mongo["training"].insert_many(trainings)
