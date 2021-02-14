from datetime import datetime, timedelta, timezone
import urllib

from tests.fill_date_base import create_exercise, create_training, create_stage


# training dates
date_1 = datetime.now(timezone.utc) - timedelta(days=2)
date_2 = datetime.now(timezone.utc) - timedelta(days=1)
date_3 = datetime.now(timezone.utc) + timedelta(hours=10)
date_4 = datetime.now(timezone.utc) + timedelta(days=1)
date_5 = datetime.now(timezone.utc) + timedelta(days=2)
date_6 = datetime.now(timezone.utc) + timedelta(days=3)
date_7 = datetime.now(timezone.utc) + timedelta(days=4)
date_8 = datetime.now(timezone.utc) + timedelta(days=5, hours=1)


def test_get_list_all(client, mongo):
    fill_cololections(mongo)
    response = client.get("/api/v1/trainings")

    assert response.status_code == 200
    trainings = response.get_json()
    assert len(trainings) == 5

    assert date_3.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[0]["date_time"]
    ).replace(microsecond=0, tzinfo=None)

    assert date_4.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[1]["date_time"]
    ).replace(microsecond=0, tzinfo=None)

    assert date_5.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[2]["date_time"]
    ).replace(microsecond=0, tzinfo=None)

    assert date_6.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[3]["date_time"]
    ).replace(microsecond=0, tzinfo=None)

    assert date_7.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[4]["date_time"]
    ).replace(microsecond=0, tzinfo=None)


def test_get_list(client, mongo):
    fill_cololections(mongo)

    url_params = urllib.parse.urlencode(
        {"category": "18U", "start": date_2.isoformat(), "end": date_6.isoformat()}
    )

    response = client.get("/api/v1/trainings?" + url_params)

    assert response.status_code == 200
    trainings = response.get_json()
    assert len(trainings) == 4

    assert date_2.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[0]["date_time"]
    ).replace(microsecond=0, tzinfo=None)

    assert date_3.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[1]["date_time"]
    ).replace(microsecond=0, tzinfo=None)

    assert date_4.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[2]["date_time"]
    ).replace(microsecond=0, tzinfo=None)

    assert date_5.replace(microsecond=0, tzinfo=None) == datetime.fromisoformat(
        trainings[3]["date_time"]
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
    exercises_5 = [
        create_exercise("507f1f77bcf86cd799439019", section="infield"),
        create_exercise("507f1f77bcf86cd799439020", section="outfield"),
    ]
    exercises_6 = [
        create_exercise("507f1f77bcf86cd799439021", section="infield"),
        create_exercise("507f1f77bcf86cd799439022", section="outfield"),
    ]
    exercises_7 = [
        create_exercise("507f1f77bcf86cd799439023", section="infield"),
        create_exercise("507f1f77bcf86cd799439024", section="outfield"),
    ]
    exercises_8 = [
        create_exercise("507f1f77bcf86cd799439025", section="infield"),
        create_exercise("507f1f77bcf86cd799439026", section="outfield"),
    ]
    exercises = (
        exercises_1
        + exercises_2
        + exercises_3
        + exercises_4
        + exercises_5
        + exercises_6
        + exercises_7
        + exercises_8
    )

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
        stages=[stage_3], date_time=date_3, _id="11111f77bcf86cd799430003"
    )

    stage_4 = create_stage(exercises=exercises_4, duration=60)
    training_4 = create_training(
        stages=[stage_4], date_time=date_4, _id="11111f77bcf86cd799430004"
    )
    stage_5 = create_stage(exercises=exercises_5, duration=60)
    training_5 = create_training(
        stages=[stage_5], date_time=date_5, _id="11111f77bcf86cd799430005"
    )
    stage_6 = create_stage(exercises=exercises_6, duration=60)
    training_6 = create_training(
        stages=[stage_6], date_time=date_6, _id="11111f77bcf86cd799430006"
    )
    stage_7 = create_stage(exercises=exercises_7, duration=60)
    training_7 = create_training(
        stages=[stage_7], date_time=date_7, _id="11111f77bcf86cd799430007"
    )
    stage_8 = create_stage(exercises=exercises_8, duration=60)
    training_8 = create_training(
        stages=[stage_8], date_time=date_8, _id="11111f77bcf86cd799430008"
    )

    trainings = [
        training_1,
        training_2,
        training_3,
        training_4,
        training_5,
        training_6,
        training_7,
        training_8,
    ]

    mongo["training"].insert_many(trainings)
