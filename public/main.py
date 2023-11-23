import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account

from src.view.public_user_view import VistaPing, VistaSignUp, VistaLogIn, VistaValidate

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_SECRET_KEY"] = 'users_s4cret_ke1'
api = Api(app)
api.add_resource(VistaPing, "/public/ping")
api.add_resource(VistaSignUp, "/public/register")
api.add_resource(VistaLogIn, "/public/login")
api.add_resource(VistaValidate, "/public/validate")

data = os.path.abspath(os.path.dirname(__file__)) + "/firebase.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)
credentials = service_account.Credentials.from_service_account_file(data)


cors = CORS(app)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3005)
