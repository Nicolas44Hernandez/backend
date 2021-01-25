from bson.objectid import ObjectId
from datetime import datetime


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

    return {
        "duration": duration,
        "nb_exercises": len(exercises),
        "exercises": [str(exercise["_id"]) for exercise in exercises],
    }


def create_training(
    stages: [],
    date: datetime,
    _id: str = "11111f77bcf86cd799430001",
    category: str = "18U",
    place: str = "Hawks Stadium",
):

    return {
        "category": category,
        "date": date,
        "place": place,
        "nb_stages": len(stages),
        "stages": stages,
        "tags": ["tag1", "tag2", "tag3"],
    }
