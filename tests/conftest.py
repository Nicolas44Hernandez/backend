import os
import pytest
import pickle
from pymongo import MongoClient

from backend.app import create_app
from backend.extension import socketio

# from config import configs, Config
from backend.config import load_config_as_object, Struct

if "CONFIG" not in os.environ:
    os.environ["CONFIG"] = "tests/base_test_config.yml"


@pytest.fixture(scope="module")
def cfg() -> str:
    return os.getenv("CONFIG")


@pytest.fixture(scope="module")
def conf(cfg: str) -> Struct:
    return load_config_as_object(cfg)


@pytest.fixture
def app(mongo):
    """Setup the flask app"""
    return create_app()


@pytest.fixture
def client(app):
    """Setup an HTTP client"""
    return app.test_client()


@pytest.fixture
def ws_client(app):
    """Setup a socketio client"""
    ws_client = socketio.test_client(app)
    ws_client.connect(namespace="/ws/v1")

    yield ws_client

    ws_client.disconnect()


@pytest.fixture
def mongo(conf):
    """Setup a mongoDB client"""
    mongo = MongoClient(conf.MONGODB_SETTINGS["host"]).get_database()

    for name in mongo.list_collection_names():
        mongo[name].drop()

    return mongo

