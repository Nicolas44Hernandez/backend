"""Extensions module.
Each extension is initialized in the app factory located in app.py."""
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_smorest import Api
from flask_socketio import SocketIO

jwt = JWTManager()
mongo = MongoEngine()
api = Api()
socketio = SocketIO(logger=True, engineio_logger=True)