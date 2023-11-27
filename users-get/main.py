import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials

from src.view.user_view import VistaPing, VistaCandidatosReady
from src.view.user_view import VistaUserProfile
from src.view.user_view import VistaUsers
from src.view.user_view import VistaCandidatos

app = Flask(__name__)

data = os.path.abspath(os.path.dirname(__file__)) + "/firebase.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)

app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(VistaUsers, "/users-get")
api.add_resource(VistaPing, "/users-get/ping")
api.add_resource(VistaUserProfile, "/users-get/profiles")
api.add_resource(VistaCandidatos, "/users-get/<string:id_candidate>")
api.add_resource(VistaCandidatosReady, "/users-get/ready/<string:id_offer>")


cors = CORS(app)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3006)
