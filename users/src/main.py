from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials

from src.view.user_view import VistaPing
from src.view.user_view import VistaUserProfile

app = Flask(__name__)

cred = credentials.Certificate('./firebase.json')
firebase_admin.initialize_app(cred)

app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(VistaPing, "/users/ping")
api.add_resource(VistaUserProfile, "/users/profiles")


cors = CORS(app)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
