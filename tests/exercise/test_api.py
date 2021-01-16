from bson.objectid import ObjectId
from datetime import datetime


def test_put_exercise(client, mongo):

    # Create a new exercise
    response = client.put(
        "/api/v1/exercises/create",
        json={
            "name": "backhand rolling",
            "section": "infield",
            "dificulty": 3,
            "duration": 30,
            "description": "hit backhand rollings",
            "video": "https://www.youtube.com/watch?v=J-nK0fZV7-8",
        },
    )

    data = response.get_json()
    assert response.status_code == 200
    assert mongo["exercise"].count() == 1
    assert data["name"] == "backhand rolling"
    assert data["section"] == "infield"
    assert data["dificulty"] == 3
    assert data["duration"] == 30
    assert data["description"] == "hit backhand rollings"
    assert data["video"] == "https://www.youtube.com/watch?v=J-nK0fZV7-8"
    # TODO: get exercise list and validate


def test_put_exercise_invalid(client):

    response = client.put(
        "/api/v1/exercises/create",
        json={"invalid": {"tal": {"tal5": 1, "ta65": 1, "taa": 1}}},
    )

    data = response.get_json()
    assert response.status_code == 422
    assert data["code"] == 422
    assert data["status"] == "Unprocessable Entity"


def test_get_list(client, mongo):
    """Should return exercises with specific IDs"""

    # init the collection
    mongo["exercise"].insert_many(
        [
            create_exercise("507f1f77bcf86cd799439011"),
            create_exercise("507f1f77bcf86cd799439012"),
            create_exercise("507f1f77bcf86cd799439013"),
        ]
    )

    # get all exercises
    response = client.get("/api/v1/exercises")

    assert response.status_code == 200
    assert len(response.get_json()) == 3
    exercises = response.get_json()
    assert exercises[0]["id"] == "507f1f77bcf86cd799439011"
    assert exercises[1]["id"] == "507f1f77bcf86cd799439012"
    assert exercises[2]["id"] == "507f1f77bcf86cd799439013"


def test_get_list_paging_default(client, mongo):
    """Should return the number of exercises corresponding to the page"""
    # init the collection
    mongo["exercise"].insert_many(
        [
            create_exercise("507f1f77bcf86cd799439001"),
            create_exercise("507f1f77bcf86cd799439002"),
            create_exercise("507f1f77bcf86cd799439003"),
            create_exercise("507f1f77bcf86cd799439004"),
            create_exercise("507f1f77bcf86cd799439005"),
            create_exercise("507f1f77bcf86cd799439006"),
            create_exercise("507f1f77bcf86cd799439007"),
            create_exercise("507f1f77bcf86cd799439008"),
            create_exercise("507f1f77bcf86cd799439009"),
            create_exercise("507f1f77bcf86cd799439010"),
            create_exercise("507f1f77bcf86cd799439011"),
            create_exercise("507f1f77bcf86cd799439012"),
            create_exercise("507f1f77bcf86cd799439013"),
            create_exercise("507f1f77bcf86cd799439014"),
            create_exercise("507f1f77bcf86cd799439015"),
            create_exercise("507f1f77bcf86cd799439016"),
            create_exercise("507f1f77bcf86cd799439017"),
            create_exercise("507f1f77bcf86cd799439018"),
            create_exercise("507f1f77bcf86cd799439019"),
            create_exercise("507f1f77bcf86cd799439020"),
            create_exercise("507f1f77bcf86cd799439021"),
        ]
    )
    # get all exercises
    response = client.get("/api/v1/exercises")

    assert response.status_code == 200
    assert len(response.get_json()) == 10


def test_get_list_paging(client, mongo):
    """Should return the number of exercises corresponding to the page"""
    # init the collection
    mongo["exercise"].insert_many(
        [
            create_exercise("507f1f77bcf86cd799439001"),
            create_exercise("507f1f77bcf86cd799439002"),
            create_exercise("507f1f77bcf86cd799439003"),
            create_exercise("507f1f77bcf86cd799439004"),
            create_exercise("507f1f77bcf86cd799439005"),
            create_exercise("507f1f77bcf86cd799439006"),
            create_exercise("507f1f77bcf86cd799439007"),
            create_exercise("507f1f77bcf86cd799439008"),
            create_exercise("507f1f77bcf86cd799439009"),
            create_exercise("507f1f77bcf86cd799439010"),
            create_exercise("507f1f77bcf86cd799439011"),
            create_exercise("507f1f77bcf86cd799439012"),
            create_exercise("507f1f77bcf86cd799439013"),
            create_exercise("507f1f77bcf86cd799439014"),
            create_exercise("507f1f77bcf86cd799439015"),
            create_exercise("507f1f77bcf86cd799439016"),
            create_exercise("507f1f77bcf86cd799439017"),
            create_exercise("507f1f77bcf86cd799439018"),
            create_exercise("507f1f77bcf86cd799439019"),
            create_exercise("507f1f77bcf86cd799439020"),
            create_exercise("507f1f77bcf86cd799439021"),
        ]
    )
    # get all exercises
    response = client.get("/api/v1/exercises?page=1&page_size=5")

    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_list_section(client, mongo):
    """Should return exercises for an specific section"""

    # init the collection
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

    # get outfield exercises
    response = client.get("/api/v1/exercises?section=outfield")

    assert response.status_code == 200
    assert len(response.get_json()) == 2
    exercises = response.get_json()
    assert exercises[0]["section"] == "outfield"
    assert exercises[1]["section"] == "outfield"


def test_get_exercise_by_id(client, mongo):
    """Should return exercise for an specific ID"""

    # init the collection
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

    # get exercise
    response = client.get("/api/v1/exercises/507f1f77bcf86cd799439013")

    assert response.status_code == 200
    exercise = response.get_json()
    assert exercise["id"] == "507f1f77bcf86cd799439013"


def test_remove_exercise_by_id(client, mongo):
    """Should return exercise for an specific ID"""

    # init the collection
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

    # delete exercise
    response = client.delete("/api/v1/exercises/507f1f77bcf86cd799439013")

    assert response.status_code == 200

    # get all exercises for verify suppression
    response = client.get("/api/v1/exercises")

    assert response.status_code == 200
    assert len(response.get_json()) == 5
    exercises = response.get_json()

    for exercise in exercises:
        assert exercise["id"] != "507f1f77bcf86cd799439013"


def create_exercise(_id: str, section: str = "infield"):
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
